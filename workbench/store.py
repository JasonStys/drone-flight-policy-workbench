"""Jason Stys: atomic policy versions, private evidence and independently reviewed snapshots. Lines: docs/SOURCE_MAP.md."""

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

from fastapi import HTTPException

from workbench.models import Policy


def canonical(value):
    """Stable JSON encoding for deterministic content identities, not digital signatures."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    """Detect accidental snapshot changes; a machine administrator remains trusted."""
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def now():
    """Record real UTC audit time separately from the operation's synthetic evaluation clock."""
    return datetime.now(UTC).isoformat()


class Store:
    """A local organization workspace; operators see their own evidence, designated reviewers/admins see all."""

    def __init__(self, path: Path):
        """Create a private local schema idempotently without resetting policy/history."""
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript(Path(__file__).with_name("schema.sql").read_text(encoding="utf-8"))

    @contextmanager
    def connect(self, write=False):
        """Serialize writers and always close, committing only complete successful transactions."""
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        try:
            if write:
                db.execute("BEGIN IMMEDIATE")
            yield db
            if write:
                db.commit()
        finally:
            db.close()

    def event(self, db, actor, event, version, detail):
        """Append non-secret structured audit evidence in the same state transaction."""
        db.execute(
            "INSERT INTO audit(at,actor,event,version,detail) VALUES(?,?,?,?,?)",
            (now(), actor, event, version, detail),
        )

    def initialize(self, policy: Policy):
        """Seed only an empty workspace; later initialization never overwrites existing records."""
        with self.connect(True) as db:
            if db.execute("SELECT 1 FROM workspace").fetchone():
                return
            db.execute(
                "INSERT INTO policies VALUES(1,?,?,?,?)",
                (policy.model_dump_json(), digest(policy.model_dump()), "local-init", now()),
            )
            db.execute("INSERT INTO workspace VALUES(1,1,1)")
            self.event(db, "local-init", "policy_initialized", 1, policy.name)

    def snapshot(self, db=None):
        """Return a coherent active immutable version or visibly fail an uninitialized install."""
        if db is None:
            with self.connect() as connection:
                return self.snapshot(connection)
        row = db.execute(
            "SELECT policies.* FROM policies JOIN workspace ON version=active_version WHERE workspace.id=1"
        ).fetchone()
        if row is None:
            raise HTTPException(503, "Initialize the local workspace first")
        policy = Policy.model_validate_json(row["content"])
        if digest(policy.model_dump()) != row["digest"]:
            raise HTTPException(503, "Policy integrity check failed")
        return row["version"], policy

    def publish(self, expected, policy, actor):
        """Compare-and-swap active version; previous policies/reviews remain immutable evidence."""
        with self.connect(True) as db:
            version, _ = self.snapshot(db)
            if expected != version:
                raise HTTPException(409, "Policy changed; refresh before publishing")
            version += 1
            db.execute(
                "INSERT INTO policies VALUES(?,?,?,?,?)",
                (version, policy.model_dump_json(), digest(policy.model_dump()), actor, now()),
            )
            db.execute("UPDATE workspace SET active_version=? WHERE id=1", (version,))
            self.event(db, actor, "policy_published", version, policy.name)
            return version

    def save(self, version, operation, result, actor):
        """Reject concurrent policy changes and atomically persist exactly the evaluated snapshot."""
        with self.connect(True) as db:
            active, policy = self.snapshot(db)
            if active != version:
                raise HTTPException(409, "Policy changed during evaluation; evaluate again")
            content = {
                "version": version,
                "policy": policy.model_dump(),
                "operation": operation.model_dump(),
                "result": result,
            }
            cursor = db.execute(
                "INSERT INTO evaluations(version,creator,operation,result,digest,created) VALUES(?,?,?,?,?,?)",
                (
                    version,
                    actor,
                    operation.model_dump_json(),
                    canonical(result),
                    digest(content),
                    now(),
                ),
            )
            self.event(db, actor, "evaluation_saved", version, str(cursor.lastrowid))
            return cursor.lastrowid

    def get(self, identifier, user, db=None):
        """Enforce object-level access and verify original policy/input/result hashes before export/review."""
        if db is None:
            with self.connect() as connection:
                return self.get(identifier, user, connection)
        row = db.execute(
            "SELECT evaluations.*,content AS policy FROM evaluations JOIN policies USING(version) WHERE id=?",
            (identifier,),
        ).fetchone()
        if row is None or (user["role"] == "operator" and row["creator"] != user["name"]):
            raise HTTPException(404, "Evaluation not found")
        result = dict(row)
        for key in ("operation", "result", "policy"):
            result[key] = json.loads(result[key])
        if (
            digest({key: result[key] for key in ("version", "operation", "result", "policy")})
            != result["digest"]
        ):
            raise HTTPException(503, "Evaluation integrity check failed")
        active, _ = self.snapshot(db)
        result["stale"] = result["version"] != active
        review = db.execute(
            "SELECT actor,decision,note,created FROM reviews WHERE evaluation=?", (identifier,)
        ).fetchone()
        result["review"] = dict(review) if review else None
        result["flight_authorization"] = False
        return result

    def review(self, identifier, user, decision, note):
        """Independent current-version sign-off cannot override blocked or unknown evidence."""
        with self.connect(True) as db:
            report = self.get(identifier, user, db)
            if report["creator"] == user["name"]:
                raise HTTPException(403, "A different reviewer is required")
            if report["review"]:
                raise HTTPException(409, "Evaluation already reviewed")
            if report["stale"]:
                raise HTTPException(409, "Policy changed; evaluate again")
            if decision == "acknowledge" and report["result"]["status"] != "satisfied":
                raise HTTPException(409, "Blocked or unknown evidence cannot be overridden")
            db.execute(
                "INSERT INTO reviews VALUES(?,?,?,?,?)",
                (identifier, user["name"], decision, note, now()),
            )
            self.event(
                db,
                user["name"],
                "human_review_recorded",
                report["version"],
                f"{identifier}: {decision}",
            )

    def history(self, user):
        """Bound history queries; operators cannot enumerate another operator's evidence or audit."""
        with self.connect() as db:
            if user["role"] == "operator":
                rows = db.execute(
                    "SELECT id,version,creator,created FROM evaluations WHERE creator=? ORDER BY id DESC LIMIT 30",
                    (user["name"],),
                )
                events = []
            else:
                rows = db.execute(
                    "SELECT id,version,creator,created FROM evaluations ORDER BY id DESC LIMIT 30"
                )
                events = [
                    dict(r) for r in db.execute("SELECT * FROM audit ORDER BY id DESC LIMIT 60")
                ]
            return [dict(r) for r in rows], events

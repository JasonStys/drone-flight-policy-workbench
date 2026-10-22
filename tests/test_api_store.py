"""Jason Stys: actual OPA/SQLite/API role, privacy, rollback and review races. Lines: docs/SOURCE_MAP.md."""

import asyncio
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from workbench import api, auth
from workbench.examples import example_operation, example_policy
from workbench.store import Store

PASSWORD = "synthetic-test-password-only"
ORIGIN = "http://127.0.0.1:8881"


@pytest.fixture
def application(tmp_path):
    """Isolated private database with designated local staff, never production accounts."""
    app = api.create_app(tmp_path / "test.sqlite3")
    app.state.store.initialize(example_policy())
    for name, role in [
        ("admin", "admin"),
        ("operator", "operator"),
        ("other", "operator"),
        ("reviewer", "reviewer"),
    ]:
        auth.add_user(app.state.store, name, PASSWORD, role)
    return app


def client(app, name="operator"):
    """Authenticate against actual Argon2/session logic and use the returned real CSRF token."""
    value = TestClient(app, base_url=ORIGIN)
    response = value.post(
        "/api/login", json={"username": name, "password": PASSWORD}, headers={"Origin": ORIGIN}
    )
    assert response.status_code == 200
    value.headers.update({"Origin": ORIGIN, "X-CSRF-Token": response.json()["csrf"]})
    return value


def evaluate(value, operation=None):
    """Submit to the real API/native engine using the currently active policy version."""
    version = value.get("/api/workspace").json()["version"]
    return value.post(
        "/api/evaluations",
        json={"version": version, "operation": (operation or example_operation()).model_dump()},
    )


def test_end_to_end_independent_acknowledgement(application):
    """A different designated reviewer can acknowledge current configured evidence, not grant permission."""
    operator = client(application)
    reviewer = client(application, "reviewer")
    response = evaluate(operator)
    assert response.status_code == 200
    identifier = response.json()["id"]
    report = operator.get(f"/api/evaluations/{identifier}").json()
    assert (
        len(report["digest"]) == 64
        and not report["stale"]
        and report["flight_authorization"] is False
    )
    reviewed = reviewer.post(
        f"/api/evaluations/{identifier}/review",
        json={"decision": "acknowledge", "note": "Independent synthetic review"},
    )
    assert reviewed.status_code == 200 and reviewed.json()["flight_authorization"] is False
    assert operator.get(f"/api/evaluations/{identifier}").json()["review"]["actor"] == "reviewer"
    assert (
        reviewer.post(
            f"/api/evaluations/{identifier}/review",
            json={"decision": "acknowledge", "note": "Duplicate"},
        ).status_code
        == 409
    )
    assert (
        operator.post(
            f"/api/evaluations/{identifier}/review",
            json={"decision": "reject", "note": "Wrong role"},
        ).status_code
        == 403
    )


def test_private_objects_and_roles(application):
    """No operator can enumerate/export another's reports; only admins change policies."""
    operator = client(application)
    other = client(application, "other")
    admin = client(application, "admin")
    identifier = evaluate(operator).json()["id"]
    assert other.get(f"/api/evaluations/{identifier}").status_code == 404
    assert other.get("/api/workspace").json()["history"] == []
    assert operator.get("/api/workspace").json()["audit"] == []
    assert admin.get(f"/api/evaluations/{identifier}").status_code == 200
    assert other.get("/api/evaluations/99999").status_code == 404
    payload = {"expected_version": 1, "policy": example_policy().model_dump()}
    assert operator.post("/api/policies", json=payload).status_code == 403
    assert admin.post("/api/policies", json=payload).status_code == 200
    assert admin.post("/api/policies", json=payload).status_code == 409
    assert operator.get(f"/api/evaluations/{identifier}").json()["stale"]
    assert (
        operator.post(
            "/api/evaluations", json={"version": 1, "operation": example_operation().model_dump()}
        ).status_code
        == 409
    )
    assert (
        client(application, "reviewer")
        .post(
            f"/api/evaluations/{identifier}/review",
            json={"decision": "acknowledge", "note": "Stale"},
        )
        .status_code
        == 409
    )


def test_self_review_and_holds(application):
    """Roles do not let a reviewer approve their own work or override unknown/blocked results."""
    reviewer = client(application, "reviewer")
    operator = client(application)
    own = evaluate(reviewer).json()["id"]
    assert (
        reviewer.post(
            f"/api/evaluations/{own}/review", json={"decision": "acknowledge", "note": "Self"}
        ).status_code
        == 403
    )
    for status in ["blocked", "requires_review"]:
        operation = example_operation()
        operation.evidence[0].value = False if status == "blocked" else None
        identifier = evaluate(operator, operation).json()["id"]
        assert (
            reviewer.post(
                f"/api/evaluations/{identifier}/review",
                json={"decision": "acknowledge", "note": "Cannot override"},
            ).status_code
            == 409
        )
        assert (
            reviewer.post(
                f"/api/evaluations/{identifier}/review",
                json={"decision": "reject", "note": "Evidence requires correction"},
            ).status_code
            == 200
        )


def test_origin_csrf_size_and_headers(application):
    """DNS rebinding, cross-site calls, missing CSRF, oversized bodies and form posts are denied."""
    value = client(application)
    assert value.get("/healthz", headers={"Host": "evil.example"}).status_code == 400
    assert (
        value.post("/api/logout", json={}, headers={"Origin": "https://evil.example"}).status_code
        == 403
    )
    assert (
        value.post("/api/logout", json={}, headers={"Sec-Fetch-Site": "cross-site"}).status_code
        == 403
    )
    assert value.post("/api/logout", json={}, headers={"X-CSRF-Token": "wrong"}).status_code == 403
    assert value.post("/api/logout", content="{}").status_code == 415
    assert value.options("/api/logout").status_code == 405
    assert (
        value.post(
            "/api/evaluations", content=b" " * 262145, headers={"Content-Type": "application/json"}
        ).status_code
        == 413
    )
    invalid = value.post(
        "/api/login", json={"username": "operator", "password": "synthetic-secret", "extra": 1}
    )
    assert invalid.status_code == 422 and "synthetic-secret" not in invalid.text
    assert "frame-ancestors 'none'" in value.get("/").headers["content-security-policy"]
    assert value.get("/").headers["cache-control"] == "no-store"
    assert "Jason Stys" in value.get("/").text
    assert value.get("/../workbench/schema.sql").status_code == 404


def test_login_expiry_revocation_and_hashes(application):
    """No plaintext passwords or bearer tokens stored; logout and absolute expiry are enforced."""
    value = client(application)
    token = value.cookies["policy_session"]
    assert value.get("/api/me").status_code == 200
    with application.state.store.connect() as db:
        assert (
            db.execute("SELECT password_hash FROM users WHERE name='operator'")
            .fetchone()[0]
            .startswith("$argon2id$")
        )
        assert db.execute("SELECT digest FROM sessions").fetchone()[0] != token
    assert value.post("/api/logout", json={}).status_code == 200
    assert value.get("/api/me").status_code == 401
    value = client(application)
    with application.state.store.connect(True) as db:
        db.execute("UPDATE sessions SET expires=0")
    assert value.get("/api/me").status_code == 401
    value.cookies.clear()
    value.cookies.set("policy_session", "short")
    assert value.get("/api/me").status_code == 401


def test_login_failures_throttle_and_cookie(application):
    """Generic invalid-credential messages and persistent attempt bounds cover unknown/existing users."""
    value = TestClient(application, base_url=ORIGIN)
    for name in ("operator", "missing"):
        assert (
            value.post(
                "/api/login",
                json={"username": name, "password": "wrong"},
                headers={"Origin": ORIGIN},
            ).status_code
            == 401
        )
    response = value.post(
        "/api/login",
        json={"username": "operator", "password": PASSWORD},
        headers={"Origin": ORIGIN},
    )
    assert (
        "HttpOnly" in response.headers["set-cookie"]
        and "SameSite=strict" in response.headers["set-cookie"]
    )
    with application.state.store.connect(True) as db:
        db.execute("UPDATE attempts SET count=20")
    assert (
        value.post(
            "/api/login",
            json={"username": "operator", "password": PASSWORD},
            headers={"Origin": ORIGIN},
        ).status_code
        == 429
    )


@pytest.mark.parametrize(
    "name,password,role",
    [
        ("Invalid", PASSWORD, "operator"),
        ("valid", "short", "operator"),
        ("valid", PASSWORD, "root"),
    ],
)
def test_provisioning_rejects_invalid(application, name, password, role):
    """No unsafe role or username provisioning through the trusted CLI helper."""
    with pytest.raises(ValueError):
        auth.add_user(application.state.store, name, password, role)


def test_session_limit_attempt_capacity_and_cleanup(application):
    """Bound per-user sessions and per-client attempt table without sleeping tests."""
    store = application.state.store
    with store.connect(True) as db:
        for n in range(12):
            db.execute(
                "INSERT INTO sessions VALUES(?,?,?,?,?)",
                (f"digest-{n}", "operator", "csrf", time.time() + 3600, n),
            )
        db.execute("INSERT INTO sessions VALUES('expired','operator','csrf',0,0)")
    client(application)
    with store.connect() as db:
        assert (
            db.execute("SELECT count(*) FROM sessions WHERE username='operator'").fetchone()[0]
            <= 11
        )
    with store.connect(True) as db:
        db.execute("DELETE FROM attempts")
        for n in range(1000):
            db.execute("INSERT INTO attempts VALUES(?,1,?)", (f"client-{n}", time.time()))
    value = TestClient(application, base_url=ORIGIN)
    assert (
        value.post(
            "/api/login",
            json={"username": "operator", "password": PASSWORD},
            headers={"Origin": ORIGIN},
        ).status_code
        == 429
    )


def test_engine_and_stale_persistence(application, monkeypatch):
    """Worker failure and concurrent active-policy changes never save a falsely current report."""
    value = client(application)

    def fail(*args):
        """Failure boundary only; other API tests execute real OPA."""
        raise api.EngineUnavailable("Synthetic unavailability")

    monkeypatch.setattr(api, "evaluate", fail)
    assert evaluate(value).status_code == 503

    def concurrent(policy, operation):
        """Inject a real policy publication while evaluation is in flight."""
        application.state.store.publish(1, example_policy(), "admin")
        return {"status": "satisfied", "checks": [], "flight_authorization": False}

    monkeypatch.setattr(api, "evaluate", concurrent)
    assert evaluate(value).status_code == 409
    assert value.get("/api/workspace").json()["history"] == []


def test_atomic_version_race_and_immutable_rows(application):
    """Exactly one concurrent publisher wins; triggers prevent history modification/deletion."""
    store = application.state.store

    def publish():
        """Race two OS-authorized workers against the same expected version."""
        try:
            return store.publish(1, example_policy(), "admin")
        except HTTPException as error:
            return error.status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(lambda _: publish(), range(2))) == [2, 409]
    store.initialize(example_policy())
    assert store.snapshot()[0] == 2
    user = {"name": "operator", "role": "operator"}
    identifier = store.save(2, example_operation(), {"status": "satisfied"}, "operator")
    store.review(identifier, {"name": "reviewer", "role": "reviewer"}, "acknowledge", "Independent")
    for statement in (
        "UPDATE policies SET version=version",
        "DELETE FROM policies",
        "UPDATE evaluations SET id=id",
        "DELETE FROM evaluations",
        "UPDATE reviews SET evaluation=evaluation",
        "DELETE FROM reviews",
    ):
        with pytest.raises(sqlite3.IntegrityError), store.connect(True) as db:
            db.execute(statement)
    assert store.get(identifier, user)["review"]


def test_corruption_missing_install_and_slow_body(application, tmp_path, monkeypatch):
    """Integrity failures, missing installation and deadline timeout are visible, not positive defaults."""
    empty = Store(tmp_path / "empty.sqlite3")
    with pytest.raises(HTTPException):
        empty.snapshot()
    with application.state.store.connect(True) as db:
        db.execute("DROP TRIGGER immutable_policy_update")
        db.execute("UPDATE policies SET digest='corrupt'")
    with pytest.raises(HTTPException):
        application.state.store.snapshot()
    monkeypatch.setattr(api, "ROOT", tmp_path)
    assert TestClient(application, base_url=ORIGIN).get("/").status_code == 503

    class Timeout:
        """Deterministic deadline failure avoids blocking tests."""

        async def __aenter__(self):
            raise TimeoutError()

        async def __aexit__(self, *args):
            return False

    monkeypatch.setattr(asyncio, "timeout", lambda _: Timeout())
    assert (
        TestClient(application, base_url=ORIGIN)
        .post("/api/login", json={}, headers={"Origin": ORIGIN})
        .status_code
        == 408
    )


def test_evaluation_corruption(application):
    """Snapshot integrity includes the original operation, result and policy content."""
    value = client(application)
    identifier = evaluate(value).json()["id"]
    with application.state.store.connect(True) as db:
        db.execute("DROP TRIGGER immutable_evaluation_update")
        db.execute("UPDATE evaluations SET digest='corrupt'")
    assert value.get(f"/api/evaluations/{identifier}").status_code == 503


def test_origin_port_validation():
    """Unsupported listener ports are rejected before constructing a service."""
    with pytest.raises(ValueError):
        api.create_app(None, 80)

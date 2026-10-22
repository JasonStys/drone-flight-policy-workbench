"""Jason Stys: isolated synthetic acceptance/demo accounts, never production user provisioning. Lines: docs/SOURCE_MAP.md."""

import argparse
import json
import secrets
from pathlib import Path

import uvicorn

from workbench.api import create_app
from workbench.auth import add_user
from workbench.examples import example_policy
from workbench.store import Store


def prepare(directory: Path):
    """Create random disposable credentials in ignored local runtime only; never log passwords."""
    directory.mkdir(parents=True, exist_ok=True)
    db = directory / "workspace.sqlite3"
    credentials = directory / "credentials.json"
    store = Store(db)
    store.initialize(example_policy())
    if not credentials.is_file():
        values = {
            role: {"username": f"demo-{role}", "password": secrets.token_urlsafe(24)}
            for role in ("admin", "operator", "reviewer")
        }
        for role, entry in values.items():
            add_user(store, entry["username"], entry["password"], role)
        credentials.write_text(json.dumps(values), encoding="utf-8")
    return db


def main():
    """Launch a fresh named local sandbox; generated credentials are test-only, not real user data."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=Path(".runtime/browser"))
    parser.add_argument("--port", type=int, default=8882)
    args = parser.parse_args()
    db = prepare(args.directory)
    uvicorn.run(create_app(db, args.port), host="127.0.0.1", port=args.port, access_log=False)


if __name__ == "__main__":
    main()

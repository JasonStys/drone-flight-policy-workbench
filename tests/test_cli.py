"""Jason Stys: trusted CLI setup/password confirmation and loopback-only serving. Lines: docs/SOURCE_MAP.md."""

import sys

import pytest

from workbench import __main__ as cli
from workbench.store import Store


def test_cli_setup_accounts_and_serve(tmp_path, monkeypatch):
    """Exercise supported installation commands without starting a second HTTP listener."""
    path = tmp_path / "cli.sqlite3"
    monkeypatch.setattr(sys, "argv", ["workbench", "--db", str(path), "init"])
    cli.main()
    assert Store(path).snapshot()[0] == 1
    answers = iter(["synthetic-cli-password", "synthetic-cli-password"])
    monkeypatch.setattr(cli.getpass, "getpass", lambda _: next(answers))
    monkeypatch.setattr(
        sys, "argv", ["workbench", "--db", str(path), "user", "local-admin", "--role", "admin"]
    )
    cli.main()
    with Store(path).connect() as db:
        assert db.execute("SELECT role FROM users").fetchone()[0] == "admin"
    answers = iter(["synthetic-cli-password", "different-password"])
    with pytest.raises(SystemExit):
        cli.main()
    calls = []
    monkeypatch.setattr(cli.uvicorn, "run", lambda *a, **kw: calls.append(kw))
    monkeypatch.setattr(sys, "argv", ["workbench", "--db", str(path), "serve", "--port", "8883"])
    cli.main()
    assert calls[0] == {
        "host": "127.0.0.1",
        "port": 8883,
        "access_log": False,
        "proxy_headers": False,
        "limit_concurrency": 24,
    }
    monkeypatch.setattr(sys, "argv", ["workbench", "--db", str(path), "serve", "--port", "80"])
    with pytest.raises(SystemExit):
        cli.main()

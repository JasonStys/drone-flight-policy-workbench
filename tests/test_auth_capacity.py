"""Jason Stys: resource-bound password verification and authentication edge cases. Lines: docs/SOURCE_MAP.md."""

from fastapi.testclient import TestClient

from workbench import auth
from workbench.api import create_app
from workbench.examples import example_policy


def test_verification_capacity_and_unknown_dummy(tmp_path):
    """No more than two memory-hard password checks; dummy match never authenticates an absent user."""
    app = create_app(tmp_path / "capacity.sqlite3")
    app.state.store.initialize(example_policy())
    value = TestClient(app, base_url="http://127.0.0.1:8881")
    auth.VERIFY_GATE.acquire()
    auth.VERIFY_GATE.acquire()
    try:
        response = value.post(
            "/api/login",
            json={"username": "missing", "password": "synthetic"},
            headers={"Origin": "http://127.0.0.1:8881"},
        )
        assert response.status_code == 429
    finally:
        auth.VERIFY_GATE.release()
        auth.VERIFY_GATE.release()
    response = value.post(
        "/api/login",
        json={"username": "missing", "password": "not-a-user-timing-equalizer"},
        headers={"Origin": "http://127.0.0.1:8881"},
    )
    assert response.status_code == 401
    assert value.get("/healthz").json()["status"] == "ok"
    assert value.get("/api/examples").status_code == 401

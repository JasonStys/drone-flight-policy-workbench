"""Jason Stys: resource-bound password verification and authentication edge cases. Lines: docs/SOURCE_MAP.md."""

import socket
import threading
import time

import httpx
import uvicorn
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


def test_real_server_forwarded_addresses_do_not_bypass_throttle(tmp_path):
    """Actual Uvicorn/HTTP requests: forged forwarded IPs cannot rotate the direct-client limit."""
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    port = listener.getsockname()[1]
    origin = f"http://127.0.0.1:{port}"
    app = create_app(tmp_path / "forwarding.sqlite3", port)
    server = uvicorn.Server(
        uvicorn.Config(
            app,
            host="127.0.0.1",
            port=port,
            proxy_headers=False,
            access_log=False,
            log_level="error",
        )
    )
    thread = threading.Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 5
        while not server.started and time.monotonic() < deadline:
            time.sleep(0.02)
        assert server.started, "Actual HTTP service failed to start"
        with httpx.Client(base_url=origin, timeout=5, trust_env=False) as value:
            for n in range(21):
                response = value.post(
                    "/api/login",
                    json={"username": "missing", "password": "synthetic-wrong-password"},
                    headers={"Origin": origin, "X-Forwarded-For": f"192.0.2.{n + 1}"},
                )
                assert response.status_code == (401 if n < 20 else 429)
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        listener.close()
    assert not thread.is_alive(), "Actual HTTP test left a server running"

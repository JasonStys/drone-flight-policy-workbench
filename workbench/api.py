"""Jason Stys: local authenticated, same-origin policy/evidence application. Lines: docs/SOURCE_MAP.md."""

import asyncio
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from workbench import auth
from workbench.engine import ROOT, EngineUnavailable, evaluate
from workbench.examples import examples
from workbench.models import Evaluate, Login, Publish, Review
from workbench.store import Store

HEADERS = {
    "Content-Security-Policy": "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}


def create_app(database: Path, port=8881):
    """One local organization, never a public multi-tenant or unauthenticated remote service."""
    if not 1024 <= port <= 65535:
        raise ValueError("Port outside supported range")
    origin = f"http://127.0.0.1:{port}"
    authority = urlsplit(origin).netloc
    app = FastAPI(
        title="Drone Flight Policy Workbench", docs_url=None, redoc_url=None, openapi_url=None
    )
    app.state.store = Store(database)

    @app.middleware("http")
    async def boundary(request: Request, call_next):
        """Exact Host/Origin, streamed body size/deadline, JSON-only writes and strict security headers."""
        response = None
        if request.headers.get("host") != authority:
            response = JSONResponse({"detail": "Untrusted Host"}, status_code=400)
        elif request.method not in {"GET", "HEAD", "POST"}:
            response = JSONResponse({"detail": "Method not allowed"}, status_code=405)
        elif request.method == "POST":
            if (
                request.headers.get("origin") != origin
                or request.headers.get("sec-fetch-site") == "cross-site"
            ):
                response = JSONResponse({"detail": "Exact same-origin required"}, status_code=403)
            elif request.headers.get("content-type", "").split(";")[0] != "application/json":
                response = JSONResponse({"detail": "JSON required"}, status_code=415)
            else:
                chunks = []
                size = 0
                try:
                    async with asyncio.timeout(5):
                        async for chunk in request.stream():
                            size += len(chunk)
                            if size > 262144:
                                response = JSONResponse(
                                    {"detail": "Body exceeds 256 KiB"}, status_code=413
                                )
                                break
                            chunks.append(chunk)
                    if response is None:
                        request._body = b"".join(chunks)
                except TimeoutError:
                    response = JSONResponse({"detail": "Body timeout"}, status_code=408)
        if response is None:
            response = await call_next(request)
        response.headers.update(HEADERS)
        return response

    @app.exception_handler(RequestValidationError)
    async def invalid(_request, error):
        """Return field/type information without reflecting passwords or evidence values."""
        return JSONResponse(
            {
                "detail": "Invalid fields, types, bounds, duplicate IDs or contradictory policy",
                "fields": [{"location": list(e["loc"]), "type": e["type"]} for e in error.errors()],
            },
            status_code=422,
        )

    @app.get("/healthz")
    def health():
        """Anonymous liveness only; no account, evidence or database paths."""
        return {"status": "ok", "mode": "synthetic-local-review"}

    @app.post("/api/login")
    def login(body: Login, request: Request):
        """Issue an opaque, HttpOnly, SameSite Strict local cookie; store only its hash."""
        token, user = auth.sign_in(request, body.username, body.password)
        response = JSONResponse(user)
        response.set_cookie("policy_session", token, httponly=True, samesite="strict", max_age=3600)
        return response

    @app.get("/api/me")
    def me(request: Request):
        """Resolve server-side session role, not client-submitted role claims."""
        return auth.identity(request)

    @app.post("/api/logout")
    def logout(request: Request):
        """Revoke this session immediately; leave other users/sessions untouched."""
        auth.sign_out(request)
        response = JSONResponse({"signed_out": True})
        response.delete_cookie("policy_session")
        return response

    @app.get("/api/workspace")
    def workspace(request: Request):
        """Share active policy with staff, but scope operator history to its creator."""
        user = auth.identity(request)
        version, policy = app.state.store.snapshot()
        history, audit = app.state.store.history(user)
        return {
            "version": version,
            "policy": policy.model_dump(),
            "history": history,
            "audit": audit,
        }

    @app.get("/api/examples")
    def templates(request: Request):
        """Four original, unlocated fictional cases; no actual approval/document lookup."""
        auth.identity(request)
        return examples()

    @app.post("/api/policies")
    def publish(body: Publish, request: Request):
        """Administrator-only immutable compare-and-swap version publication."""
        user = auth.authorize(request, "admin")
        return {
            "version": app.state.store.publish(body.expected_version, body.policy, user["name"])
        }

    @app.post("/api/evaluations")
    def assess(body: Evaluate, request: Request):
        """Run real OPA and save only if the exact policy remains active afterward."""
        user = auth.authorize(request)
        version, policy = app.state.store.snapshot()
        if version != body.version:
            raise HTTPException(409, "Policy changed; refresh")
        try:
            result = evaluate(policy, body.operation)
        except EngineUnavailable as error:
            raise HTTPException(503, str(error)) from error
        identifier = app.state.store.save(version, body.operation, result, user["name"])
        return {"id": identifier, "result": result}

    @app.get("/api/evaluations/{identifier}")
    def report(identifier: int, request: Request):
        """Portable immutable evidence includes original policy, input, hash and explicit stale state."""
        return app.state.store.get(identifier, auth.identity(request))

    @app.post("/api/evaluations/{identifier}/review")
    def review(identifier: int, body: Review, request: Request):
        """Independent reviewer cannot acknowledge stale, blocked or incomplete evidence."""
        user = auth.authorize(request, "reviewer")
        app.state.store.review(identifier, user, body.decision, body.note)
        return {"review_recorded": True, "flight_authorization": False}

    @app.get("/")
    def index():
        """Deliver fixed built UI; no arbitrary local file reads."""
        if not (ROOT / "dist/index.html").is_file():
            raise HTTPException(503, "Build UI with npm run build")
        return FileResponse(ROOT / "dist/index.html")

    if (ROOT / "dist/assets").is_dir():
        app.mount("/assets", StaticFiles(directory=ROOT / "dist/assets"), name="assets")
    return app

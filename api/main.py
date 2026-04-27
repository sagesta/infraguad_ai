"""FastAPI service: status, alerts, health, auth, threats, runbooks, and dashboard."""

from __future__ import annotations

import hmac
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


def _load_env() -> None:
    root = Path(__file__).resolve().parents[1]
    load_dotenv(root / ".env")


_load_env()

from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from api import store
from api.auth import PUBLIC_PATHS, create_session_token, validate_session_token
from api.middleware.audit import AuditMiddleware
from api.middleware.rate_limit import limiter
from api.middleware.security import SecurityHeadersMiddleware


# --- Auth Middleware ---

class AuthMiddleware(BaseHTTPMiddleware):
    """Redirect unauthenticated requests to /login."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path.rstrip("/") or "/"

        # Public paths skip auth
        if path in PUBLIC_PATHS:
            return await call_next(request)

        # Static assets for login page
        if path.startswith("/login"):
            return await call_next(request)

        # Check session cookie
        session = request.cookies.get("session")
        if session:
            payload = validate_session_token(session)
            if payload:
                return await call_next(request)

        # API requests get 401, browser requests get redirected
        if path.startswith("/api/"):
            return JSONResponse({"error": "unauthorized"}, status_code=401)
        return RedirectResponse("/login", status_code=302)


# --- App Setup ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    await store.init_db()
    yield


app = FastAPI(title="InfraGuard AI API", lifespan=lifespan)

# Register middleware (order matters — outermost first)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuditMiddleware)
app.add_middleware(AuthMiddleware)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# --- Auth Routes ---


def _login_page_path() -> Path:
    return Path(__file__).resolve().parents[1] / "dashboard" / "login.html"


def _login_error_response() -> HTMLResponse:
    text = _login_page_path().read_text(encoding="utf-8")
    text = text.replace(
        '<div class="error-msg" id="errorMsg"></div>',
        '<div class="error-msg" id="errorMsg">Invalid credentials</div>',
        1,
    )
    return HTMLResponse(text)


@app.get("/login")
async def login_page() -> FileResponse:
    return FileResponse(_login_page_path())


@app.post("/login")
async def login_submit(request: Request) -> Response:
    form = await request.form()
    username = str(form.get("username", "")).strip()
    password = str(form.get("password", "")).strip()
    expected_user = (os.environ.get("INFRAGUARD_USERNAME") or "").strip()
    expected_pass = (os.environ.get("INFRAGUARD_PASSWORD") or "").strip()

    if (
        username
        and password
        and expected_user
        and expected_pass
        and hmac.compare_digest(username, expected_user)
        and hmac.compare_digest(password, expected_pass)
    ):
        token = create_session_token(username)
        response = RedirectResponse("/", status_code=302)
        response.set_cookie(
            "session",
            token,
            httponly=True,
            samesite="lax",
            max_age=86400,
        )
        return response

    return _login_error_response()


@app.get("/logout")
async def logout() -> Response:
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("session")
    return response


# --- Existing Routes ---

@app.get("/status")
async def get_status() -> JSONResponse:
    latest = await store.fetch_latest_verdict()
    if not latest:
        return JSONResponse({"verdict": None})
    payload = latest.get("payload") or {}
    verdict = payload.get("verdict") if isinstance(payload, dict) else None
    return JSONResponse(
        {
            "created_at": latest.get("created_at"),
            "severity": latest.get("severity"),
            "summary": latest.get("summary"),
            "verdict": verdict,
            "extras": payload.get("extras") if isinstance(payload, dict) else None,
        }
    )


@app.get("/alerts")
async def get_alerts() -> JSONResponse:
    rows = await store.fetch_recent_verdicts(20)
    alerts: list[dict[str, Any]] = []
    for row in rows:
        alerts.append(
            {
                "id": row.get("id"),
                "created_at": row.get("created_at"),
                "severity": row.get("severity"),
                "summary": row.get("summary"),
            }
        )
    return JSONResponse({"alerts": alerts})


@app.get("/health")
async def health() -> JSONResponse:
    last = await store.fetch_last_check_iso()
    agent = "unknown"
    if last:
        ts = datetime.fromisoformat(last)
        age = (datetime.now(timezone.utc) - ts).total_seconds()
        agent = "running" if age <= 120 else "stale"
    return JSONResponse({
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "last_check": last,
    })


# --- Agent Mode ---

@app.get("/api/agent/mode")
async def get_agent_mode() -> JSONResponse:
    mode = "langchain" if os.environ.get("USE_LANGCHAIN_AGENT", "").strip() == "1" else "gemini_direct"
    return JSONResponse({"mode": mode, "model": "gemini-2.5-flash"})


# --- Threat Routes ---

@app.get("/api/threats")
async def get_threats() -> JSONResponse:
    from agent.tools.threat_response import analyze_threats

    # Try to get recent logs from the last verdict for threat analysis
    latest = await store.fetch_latest_verdict()
    loki_logs: list[dict[str, Any]] = []

    if latest:
        payload = latest.get("payload") or {}
        if isinstance(payload, dict):
            extras = payload.get("extras") or {}
            if isinstance(extras, dict):
                raw_llm = extras.get("raw_llm", "")
                # Use docker log errors if available
                verdict = payload.get("verdict") or {}
                root_cause = str(verdict.get("root_cause", ""))
                if root_cause:
                    loki_logs.append({"line": root_cause})

    result = analyze_threats(loki_logs)
    return JSONResponse(result)


@app.post("/api/threats/apply")
async def apply_threat_decision(request: Request) -> JSONResponse:
    from agent.tools.threat_response import apply_crowdsec_decision

    body = await request.json()
    decision = body.get("decision", {})
    result = apply_crowdsec_decision(decision)
    return JSONResponse(result)


# --- Runbook Routes ---

@app.post("/api/runbooks/query")
async def query_runbooks_api(request: Request) -> JSONResponse:
    from agent.rag.runbook_agent import query_runbooks

    body = await request.json()
    question = str(body.get("question", "")).strip()
    if not question:
        return JSONResponse({"ok": False, "error": "missing_question"}, status_code=400)

    result = query_runbooks(question)
    return JSONResponse(result)


@app.get("/api/runbooks/index")
async def index_runbooks() -> JSONResponse:
    from agent.rag.notion_loader import load_notion_runbooks
    from agent.rag.vector_store import build_index

    docs = load_notion_runbooks()
    count = build_index(docs)
    return JSONResponse({"ok": True, "documents_indexed": count})


# --- Dashboard ---

@app.get("/")
async def dashboard() -> FileResponse:
    root = Path(__file__).resolve().parents[1]
    path = root / "dashboard" / "index.html"
    return FileResponse(path)


def create_app() -> FastAPI:
    return app

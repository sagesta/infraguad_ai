"""FastAPI service: status, alerts, health, auth, threats, runbooks, and dashboard."""

from __future__ import annotations

import asyncio
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
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from agent.llm.providers import active_model, llm_provider
from api import store
from api.auth import PUBLIC_PATHS, create_session_token, validate_session_token, verify_credentials
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

# Register middleware. Starlette wraps in reverse order: the LAST one added is
# outermost. Effective request flow: Audit (logs everything, including 401s and
# 429s) -> SecurityHeaders (headers on every response) -> RateLimit -> Auth.
app.add_middleware(AuthMiddleware)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuditMiddleware)

# Rate limiting (default 60/minute per IP; see api/middleware/rate_limit.py)
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
@limiter.limit("5/minute")
async def login_submit(request: Request) -> Response:
    form = await request.form()
    username = str(form.get("username", "")).strip()
    password = str(form.get("password", "")).strip()

    # verify_credentials computes both digests up front (no short-circuit) and
    # is the single source of truth for credential checking.
    if verify_credentials(username, password):
        token = create_session_token(username)
        response = RedirectResponse("/", status_code=302)
        response.set_cookie(
            "session",
            token,
            httponly=True,
            samesite="lax",
            max_age=86400,
            # Set SESSION_COOKIE_SECURE=1 once the dashboard is served over HTTPS.
            secure=os.environ.get("SESSION_COOKIE_SECURE", "").strip() == "1",
        )
        return response

    return _login_error_response()


@app.get("/logout")
async def logout() -> Response:
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("session")
    return response


# --- Existing Routes ---


def _current_user(request: Request) -> str:
    session = request.cookies.get("session")
    if session:
        payload = validate_session_token(session)
        if payload:
            return str(payload.get("sub", "operator"))
    return "operator"


def _heartbeat_interval_seconds() -> int:
    raw = os.environ.get("HEARTBEAT_INTERVAL_SECONDS", "").strip() or "120"
    try:
        return max(int(raw), 10)
    except ValueError:
        return 120


def _staleness(created_at: str | None) -> tuple[int | None, bool]:
    """Age of the latest verdict in seconds, and whether the agent looks dead."""
    if not created_at:
        return None, False
    try:
        created = datetime.fromisoformat(str(created_at))
    except ValueError:
        return None, False
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    age = int((datetime.now(timezone.utc) - created).total_seconds())
    # Allow up to 3 intervals of slack: one LLM cycle can take a minute on its own.
    return age, age > _heartbeat_interval_seconds() * 3


@app.get("/status")
async def get_status() -> JSONResponse:
    latest = await store.fetch_latest_verdict()
    if not latest:
        return JSONResponse({"verdict": None, "age_seconds": None, "stale": False})
    payload = latest.get("payload") or {}
    verdict = payload.get("verdict") if isinstance(payload, dict) else None
    age_seconds, stale = _staleness(latest.get("created_at"))
    return JSONResponse(
        {
            "created_at": latest.get("created_at"),
            "severity": latest.get("severity"),
            "summary": latest.get("summary"),
            "verdict": verdict,
            "extras": payload.get("extras") if isinstance(payload, dict) else None,
            "age_seconds": age_seconds,
            "stale": stale,
            "heartbeat_interval_seconds": _heartbeat_interval_seconds(),
            "fingerprint": latest.get("fingerprint"),
            "signature": latest.get("signature"),
            "acknowledged": latest.get("acknowledged", False),
            "suppressed": latest.get("suppressed", False),
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
                "fingerprint": row.get("fingerprint"),
                "signature": row.get("signature"),
                "acknowledged": row.get("acknowledged", False),
                "suppressed": row.get("suppressed", False),
            }
        )
    return JSONResponse({"alerts": alerts})


# --- Verdict Memory (acknowledge / suppress) ---

@app.post("/api/verdicts/ack")
async def ack_verdict(request: Request) -> JSONResponse:
    """Acknowledge a verdict condition as a known non-issue.

    Keyed on the fingerprint (content + ruleset version), so it auto-expires when
    the condition or the prompt/model changes. high/critical cannot be suppressed.
    """
    body = await request.json()
    fingerprint = str(body.get("fingerprint", "")).strip()
    note = str(body.get("note", "")).strip()
    if not fingerprint:
        return JSONResponse({"ok": False, "error": "missing_fingerprint"}, status_code=400)

    verdict = await store.fetch_verdict_by_fingerprint(fingerprint)
    if not verdict:
        return JSONResponse({"ok": False, "error": "unknown_fingerprint"}, status_code=404)

    severity = str(verdict.get("severity", "")).lower()
    if severity in {"high", "critical"}:
        return JSONResponse(
            {
                "ok": False,
                "error": "cannot_ack_severe",
                "message": "high/critical verdicts cannot be suppressed",
            },
            status_code=409,
        )

    result = await store.insert_ack(
        fingerprint,
        signature=str(verdict.get("signature", "")),
        severity=severity,
        summary=str(verdict.get("summary", "")),
        note=note,
        acked_by=_current_user(request),
    )
    return JSONResponse({"ok": True, **result})


@app.post("/api/verdicts/unack")
async def unack_verdict(request: Request) -> JSONResponse:
    body = await request.json()
    fingerprint = str(body.get("fingerprint", "")).strip()
    if not fingerprint:
        return JSONResponse({"ok": False, "error": "missing_fingerprint"}, status_code=400)
    await store.delete_ack(fingerprint)
    return JSONResponse({"ok": True})


@app.get("/api/acks")
async def list_acks() -> JSONResponse:
    return JSONResponse({"acks": await store.fetch_active_acks()})


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


# --- Configuration / Agent Mode ---


def _env_set(name: str) -> bool:
    return bool(os.environ.get(name, "").strip())


def _agent_mode() -> str:
    return "langchain" if os.environ.get("USE_LANGCHAIN_AGENT", "").strip() == "1" else "direct"


def _local_runbooks_configured() -> bool:
    from agent.rag.local_runbooks_loader import runbooks_configured

    return runbooks_configured()


@app.get("/api/config")
async def get_config() -> JSONResponse:
    """Which integrations are configured (booleans only — never values)."""
    return JSONResponse(
        {
            "integrations": {
                "loki": _env_set("LOKI_URL"),
                "prometheus": _env_set("PROMETHEUS_URL"),
                "http_probes": _env_set("PROBE_URLS"),
                "local_runbooks": _local_runbooks_configured(),
                "crowdsec": _env_set("CROWDSEC_API_URL"),
                "ntfy_notifications": _env_set("NTFY_TOPIC"),
                "docker_monitoring": os.environ.get("ENABLE_DOCKER_MONITORING", "").strip() == "1",
            },
            "agent_mode": _agent_mode(),
            "llm_provider": llm_provider(),
            "model": active_model(),
            "heartbeat_interval_seconds": _heartbeat_interval_seconds(),
        }
    )


@app.get("/api/agent/mode")
async def get_agent_mode() -> JSONResponse:
    return JSONResponse({"mode": _agent_mode(), "llm_provider": llm_provider(), "model": active_model()})


# --- Threat Routes ---

@app.get("/api/threats")
async def get_threats() -> JSONResponse:
    """Scan recent Loki logs for brute-force / port-scan patterns."""
    from agent.tools.loki import fetch_loki_logs
    from agent.tools.threat_response import analyze_threats

    loki_result = await asyncio.to_thread(fetch_loki_logs, 500)

    loki_logs: list[dict[str, Any]] = []
    if isinstance(loki_result, dict) and loki_result.get("ok"):
        lines = loki_result.get("lines")
        if isinstance(lines, list):
            loki_logs = lines

    result = analyze_threats(loki_logs)
    result["log_lines_scanned"] = len(loki_logs)
    result["loki_configured"] = loki_result is not None
    return JSONResponse(result)


@app.post("/api/threats/apply")
async def apply_threat_decision(request: Request) -> JSONResponse:
    """Build a CrowdSec ban decision from a detected threat and apply it.

    The decision payload is generated server-side from the threat fields, so the
    client never submits a raw CrowdSec decision. Without CROWDSEC_API_URL this
    runs in dry-run mode (logged, not applied).
    """
    from agent.tools.threat_response import apply_crowdsec_decision, suggest_crowdsec_decision

    body = await request.json()
    threat = body.get("threat") or {}
    if not isinstance(threat, dict) or not str(threat.get("source_ip", "")).strip():
        return JSONResponse({"ok": False, "error": "missing_threat"}, status_code=400)

    decision = suggest_crowdsec_decision(threat)
    result = await asyncio.to_thread(apply_crowdsec_decision, decision)
    return JSONResponse(result, status_code=200 if result.get("ok") else 502)


# --- Runbook Routes ---

@app.post("/api/runbooks/query")
async def query_runbooks_api(request: Request) -> JSONResponse:
    from agent.rag.runbook_agent import query_runbooks

    body = await request.json()
    question = str(body.get("question", "")).strip()
    if not question:
        return JSONResponse({"ok": False, "error": "missing_question"}, status_code=400)

    # The RAG chain makes a blocking LLM call; keep it off the event loop.
    result = await asyncio.to_thread(query_runbooks, question)
    return JSONResponse(result)


@app.post("/api/runbooks/index")
async def index_runbooks() -> JSONResponse:
    from agent.rag.local_runbooks_loader import load_local_runbooks
    from agent.rag.vector_store import build_index

    def _do_index() -> int:
        docs = load_local_runbooks()
        return build_index(docs)

    count = await asyncio.to_thread(_do_index)
    return JSONResponse({"ok": True, "documents_indexed": count})


# --- Dashboard ---

@app.get("/")
async def dashboard() -> FileResponse:
    root = Path(__file__).resolve().parents[1]
    path = root / "dashboard" / "index.html"
    return FileResponse(path)


def create_app() -> FastAPI:
    return app

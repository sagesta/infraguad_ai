"""Audit logging middleware — logs every request to audit.log."""

from __future__ import annotations

import logging
import time
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

# Dedicated file logger for audit trail
_audit_logger = logging.getLogger("infraguard.audit")
_audit_handler = logging.FileHandler("audit.log", encoding="utf-8")
_audit_handler.setFormatter(
    logging.Formatter("%(message)s")
)
_audit_logger.addHandler(_audit_handler)
_audit_logger.setLevel(logging.INFO)
_audit_logger.propagate = False


class AuditMiddleware(BaseHTTPMiddleware):
    """Log {timestamp, ip, route, method, user, status_code} for every request."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.time()
        response = await call_next(request)
        elapsed_ms = int((time.time() - start) * 1000)

        user = "anonymous"
        session = request.cookies.get("session")
        if session:
            from api.auth import validate_session_token
            payload = validate_session_token(session)
            if payload:
                user = str(payload.get("sub", "unknown"))

        import json
        from datetime import datetime, timezone

        entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ip": request.client.host if request.client else "unknown",
            "method": request.method,
            "route": str(request.url.path),
            "status_code": response.status_code,
            "user": user,
            "elapsed_ms": elapsed_ms,
        }
        _audit_logger.info(json.dumps(entry, default=str))
        return response

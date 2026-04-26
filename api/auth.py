"""Session-based authentication for InfraGuard API."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from typing import Any

from itsdangerous import BadSignature, URLSafeTimedSerializer


_SESSION_MAX_AGE = 86400  # 24 hours


def _get_serializer() -> URLSafeTimedSerializer:
    secret = os.environ.get("SECRET_KEY", "").strip()
    if not secret:
        raise RuntimeError("SECRET_KEY environment variable must be set")
    return URLSafeTimedSerializer(secret)


def verify_credentials(username: str, password: str) -> bool:
    """Compare supplied credentials against env-var stored admin credentials."""
    expected_user = os.environ.get("INFRAGUARD_USERNAME", "").strip()
    expected_pass = os.environ.get("INFRAGUARD_PASSWORD", "").strip()
    if not expected_user or not expected_pass:
        return False
    user_ok = hmac.compare_digest(username, expected_user)
    pass_ok = hmac.compare_digest(password, expected_pass)
    return user_ok and pass_ok


def create_session_token(username: str) -> str:
    """Create a signed, timestamped session token."""
    s = _get_serializer()
    payload: dict[str, Any] = {"sub": username, "iat": int(time.time())}
    return s.dumps(payload)


def validate_session_token(token: str) -> dict[str, Any] | None:
    """Validate and decode a session token. Returns payload or None."""
    try:
        s = _get_serializer()
        payload: dict[str, Any] = s.loads(token, max_age=_SESSION_MAX_AGE)
        return payload
    except (BadSignature, Exception):
        return None


# Paths that never require authentication
PUBLIC_PATHS: set[str] = {"/health", "/login"}

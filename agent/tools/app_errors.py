"""Fetch recent application errors from DevPlanner HTTP API."""

from __future__ import annotations

import os
from typing import Any

import httpx


def _normalize_errors(body: Any) -> list[Any]:
    if isinstance(body, list):
        return body
    if isinstance(body, dict):
        for key in ("errors", "data", "items", "results"):
            val = body.get(key)
            if isinstance(val, list):
                return val
        return [body]
    return [body]


async def fetch_app_errors() -> dict[str, Any]:
    """
    GET ``{DEVPLANNER_API_URL}/errors/recent?limit=50`` and return structured output.

    Expects JSON: a list of errors, or an object containing a list under a common key.
    """
    base = os.environ.get("DEVPLANNER_API_URL", "").strip()
    if not base:
        return {
            "ok": False,
            "error": "missing_env",
            "message": "DEVPLANNER_API_URL is not set",
            "errors": [],
        }

    url = f"{base.rstrip('/')}/errors/recent?limit=50"

    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            response = await client.get(url)
    except httpx.HTTPError as exc:
        return {
            "ok": False,
            "error": "request_failed",
            "message": str(exc),
            "errors": [],
            "url": url,
        }

    if response.status_code != 200:
        return {
            "ok": False,
            "error": "http_error",
            "message": response.text[:2000],
            "status_code": response.status_code,
            "errors": [],
            "url": url,
        }

    try:
        body = response.json()
    except ValueError:
        return {
            "ok": False,
            "error": "invalid_json",
            "message": "Response was not valid JSON",
            "errors": [],
            "url": url,
            "status_code": response.status_code,
        }

    errors = _normalize_errors(body)
    return {
        "ok": True,
        "url": url,
        "status_code": response.status_code,
        "count": len(errors),
        "errors": errors,
    }

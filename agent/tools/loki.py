"""Loki log query tool."""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import urljoin

import httpx


def fetch_loki_logs() -> dict[str, Any]:
    """
    HTTP GET to Loki API; fetch up to last 50 log lines across streams.

    Returns a structured list under ``lines`` or an error dict.
    """
    base = os.environ.get("LOKI_URL", "").rstrip("/")
    if not base:
        return {"ok": False, "error": "missing_env", "message": "LOKI_URL is not set"}

    query = '{job=~".+"}'
    params = {"query": query, "limit": "50"}
    url = urljoin(base + "/", "loki/api/v1/query")

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            payload = resp.json()
    except httpx.HTTPError as exc:
        return {
            "ok": False,
            "error": "http_error",
            "message": str(exc),
        }
    except Exception as exc:  # noqa: BLE001 - tool boundary
        return {
            "ok": False,
            "error": "unexpected",
            "message": str(exc),
        }

    lines: list[dict[str, Any]] = []
    try:
        result = payload.get("data", {}).get("result", [])
        for stream in result:
            labels = stream.get("stream", {})
            values = stream.get("values", []) or []
            for ts_ns, line in values[:50]:
                lines.append({"timestamp_ns": ts_ns, "labels": labels, "line": line})
                if len(lines) >= 50:
                    break
            if len(lines) >= 50:
                break
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": "parse_error",
            "message": str(exc),
            "raw": payload,
        }

    return {"ok": True, "lines": lines, "count": len(lines)}

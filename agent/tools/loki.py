"""Loki log query tool."""

from __future__ import annotations

import os
import time
from typing import Any
from urllib.parse import urljoin

import httpx

_DEFAULT_WINDOW_MINUTES = 15


def fetch_loki_logs(limit: int = 50, window_minutes: int = _DEFAULT_WINDOW_MINUTES) -> dict[str, Any] | None:
    """
    Query Loki for the most recent log lines across all streams.

    Uses ``query_range`` over the last ``window_minutes`` with ``direction=backward``
    so results are always the newest lines in an explicit time window.

    Returns a structured list under ``lines``, an error dict, or ``None`` when
    LOKI_URL is not configured.
    """
    if not os.environ.get("LOKI_URL", "").strip():
        return None

    base = os.environ.get("LOKI_URL", "").rstrip("/")

    end_ns = time.time_ns()
    start_ns = end_ns - window_minutes * 60 * 1_000_000_000
    params = {
        "query": '{job=~".+"}',
        "limit": str(limit),
        "start": str(start_ns),
        "end": str(end_ns),
        "direction": "backward",
    }
    url = urljoin(base + "/", "loki/api/v1/query_range")

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
            for ts_ns, line in values[:limit]:
                lines.append({"timestamp_ns": ts_ns, "labels": labels, "line": line})
                if len(lines) >= limit:
                    break
            if len(lines) >= limit:
                break
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": "parse_error",
            "message": str(exc),
            "raw": payload,
        }

    return {"ok": True, "lines": lines, "count": len(lines)}

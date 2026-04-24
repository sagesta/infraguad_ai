"""HTTP endpoint probing tool."""

from __future__ import annotations

import os
import time
from typing import Any

import httpx


def probe_endpoints() -> dict[str, Any]:
    """
    GET each configured URL from PROBE_URLS (comma-separated).

    Returns status codes and latency in milliseconds per URL.
    """
    raw = os.environ.get("PROBE_URLS", "").strip()
    if not raw:
        return {}

    urls = [u.strip() for u in raw.split(",") if u.strip()]
    results: list[dict[str, Any]] = []

    try:
        with httpx.Client(timeout=15.0, follow_redirects=True) as client:
            for url in urls:
                start = time.perf_counter()
                try:
                    resp = client.get(url)
                    latency_ms = int((time.perf_counter() - start) * 1000)
                    results.append(
                        {
                            "url": url,
                            "ok": True,
                            "status_code": resp.status_code,
                            "latency_ms": latency_ms,
                        }
                    )
                except httpx.HTTPError as exc:
                    latency_ms = int((time.perf_counter() - start) * 1000)
                    results.append(
                        {
                            "url": url,
                            "ok": False,
                            "error": "http_error",
                            "message": str(exc),
                            "latency_ms": latency_ms,
                        }
                    )
                except Exception as exc:  # noqa: BLE001
                    results.append(
                        {
                            "url": url,
                            "ok": False,
                            "error": "unexpected",
                            "message": str(exc),
                        }
                    )
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": "unexpected",
            "message": str(exc),
        }

    return {"ok": True, "probes": results}

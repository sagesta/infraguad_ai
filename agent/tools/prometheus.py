"""Prometheus instant query tool."""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import urljoin

import httpx


def _instant_query(client: httpx.Client, base: str, promql: str) -> dict[str, Any]:
    url = urljoin(base + "/", "api/v1/query")
    try:
        resp = client.get(url, params={"query": promql})
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "success":
            return {"ok": False, "error": data.get("error", "query_failed"), "data": data}
        result = data.get("data", {}).get("result", [])
        return {"ok": True, "result": result}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}


def query_prometheus() -> dict[str, Any] | None:
    """
    Query Prometheus for CPU, RAM, disk, and HTTP 5xx rate style signals.

    Returns a dict of metric keys to query results (or error sub-dicts).
    """
    if not os.environ.get("PROMETHEUS_URL", "").strip():
        return None

    base = os.environ.get("PROMETHEUS_URL", "").rstrip("/")

    queries: dict[str, str] = {
        "cpu_busy_ratio": (
            "avg(rate(node_cpu_seconds_total{mode!='idle'}[5m])) "
            "/ avg(rate(node_cpu_seconds_total[5m]))"
        ),
        "memory_available_ratio": (
            "node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes"
        ),
        "disk_avail_bytes_root": (
            "node_filesystem_avail_bytes{mountpoint='/',fstype!='rootfs'}"
        ),
        "http_5xx_ratio": (
            "sum(rate(http_requests_total{status=~'5..'}[5m])) "
            "/ clamp_min(sum(rate(http_requests_total[5m])), 1)"
        ),
    }

    out: dict[str, Any] = {"ok": True, "metrics": {}}

    try:
        with httpx.Client(timeout=30.0) as client:
            for key, promql in queries.items():
                out["metrics"][key] = _instant_query(client, base, promql)
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": "unexpected",
            "message": str(exc),
        }

    return out

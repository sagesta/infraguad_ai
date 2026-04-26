"""LangChain @tool wrappers around existing InfraGuard collection tools."""

from __future__ import annotations

import json
from typing import Any

from langchain_core.tools import tool

from agent.tools.http_probe import probe_endpoints
from agent.tools.loki import fetch_loki_logs
from agent.tools.prometheus import query_prometheus


@tool
def fetch_loki_logs_tool() -> str:
    """Fetch the last 50 log lines from Loki.

    Returns a JSON string with log lines and metadata, or an error message
    if Loki is not configured.
    """
    result = fetch_loki_logs()
    if result is None:
        return json.dumps({"status": "not_configured", "message": "Loki is not configured for this deployment"})
    return json.dumps(result, default=str)


@tool
def fetch_prometheus_metrics_tool() -> str:
    """Query Prometheus for CPU, memory, disk, and HTTP error rate metrics.

    Returns a JSON string with metric values, or an error message
    if Prometheus is not configured.
    """
    result = query_prometheus()
    if result is None:
        return json.dumps({"status": "not_configured", "message": "Prometheus is not configured for this deployment"})
    return json.dumps(result, default=str)


@tool
def probe_http_endpoints_tool() -> str:
    """Probe configured HTTP endpoints and return status codes and latency.

    Returns a JSON string with probe results for each configured URL.
    """
    result = probe_endpoints()
    if not result:
        return json.dumps({"status": "not_configured", "message": "No probe URLs configured"})
    return json.dumps(result, default=str)


ALL_TOOLS = [fetch_loki_logs_tool, fetch_prometheus_metrics_tool, probe_http_endpoints_tool]

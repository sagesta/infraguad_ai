"""Prompt assembly for Vertex AI (Gemini) SRE verdicts."""

from __future__ import annotations

import json
from typing import Any


def assemble_prompt(
    loki_logs: str,
    prometheus_metrics: str,
    docker_events: str,
    probe_results: str,
    docker_logs: str,
) -> str:
    """Build the full user prompt with embedded telemetry sections."""
    return f"""
You are a senior SRE analyzing infrastructure telemetry.
Return ONLY valid JSON with these fields:
- severity: one of "ok", "warning", "high", "critical"
- summary: one sentence describing current state
- root_cause: detailed analysis of what is wrong and why
- recommended_action: specific steps to resolve

TELEMETRY DATA:
=== LOGS (last 50 lines) ===
{loki_logs}

=== METRICS (CPU/RAM/Disk) ===
{prometheus_metrics}

=== DOCKER EVENTS (last 60s) ===
{docker_events}

=== HTTP PROBE RESULTS ===
{probe_results}

=== DEVPLANNER DOCKER LOG ERRORS (keyword-filtered tail) ===
{docker_logs}
"""


def assemble_prompt_from_collected(collected: dict[str, Any]) -> str:
    """Serialize tool outputs into telemetry blocks for ``assemble_prompt``."""
    loki_logs = json.dumps(collected.get("loki"), indent=2, default=str)
    prometheus_metrics = json.dumps(collected.get("prometheus"), indent=2, default=str)
    docker_events = json.dumps(collected.get("docker"), indent=2, default=str)
    probe_results = json.dumps(collected.get("http_probe"), indent=2, default=str)
    docker_logs = json.dumps(collected.get("docker_logs"), indent=2, default=str)
    return assemble_prompt(loki_logs, prometheus_metrics, docker_events, probe_results, docker_logs)

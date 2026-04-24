"""Prompt assembly for Vertex AI (Gemini) SRE verdicts."""

from __future__ import annotations

import json
from typing import Any


def assemble_prompt_from_collected(collected: dict[str, Any]) -> str:
    """Serialize tool outputs into telemetry blocks for Gemini.

    Loki and Prometheus sections are omitted entirely when those tools were not
    collected (unconfigured URLs), so the model is not steered by missing-env payloads.
    """
    blocks: list[str] = []

    if "loki" in collected:
        blocks.append(
            "=== LOGS (last 50 lines) ===\n" + json.dumps(collected["loki"], indent=2, default=str)
        )
    if "prometheus" in collected:
        blocks.append(
            "=== METRICS (CPU/RAM/Disk) ===\n"
            + json.dumps(collected["prometheus"], indent=2, default=str)
        )

    blocks.append(
        "=== DOCKER EVENTS (last 60s) ===\n" + json.dumps(collected.get("docker"), indent=2, default=str)
    )
    blocks.append(
        "=== HTTP PROBE RESULTS ===\n" + json.dumps(collected.get("http_probe"), indent=2, default=str)
    )
    blocks.append(
        "=== DEVPLANNER DOCKER LOG ERRORS (keyword-filtered tail) ===\n"
        + json.dumps(collected.get("docker_logs"), indent=2, default=str)
    )

    telemetry = "\n\n".join(blocks)

    return f"""
You are a senior SRE analyzing infrastructure telemetry.
Return ONLY valid JSON with these fields:
- severity: one of "ok", "warning", "high", "critical"
- summary: one sentence describing current state
- root_cause: detailed analysis of what is wrong and why
- recommended_action: specific steps to resolve

TELEMETRY DATA:

{telemetry}
"""

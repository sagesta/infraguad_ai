"""Async heartbeat scheduler driving the LangGraph orchestrator."""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from agent.orchestrator import run_cycle
from agent.tools.docker_logs import fetch_container_errors
from api.store import init_db, insert_verdict


logger = logging.getLogger("infraguard.agent")
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def _load_env() -> None:
    root = Path(__file__).resolve().parents[1]
    load_dotenv(root / ".env")


async def _persist_cycle_result(final_state: dict[str, object]) -> None:
    verdict = final_state.get("verdict")
    if not isinstance(verdict, dict):
        verdict = {
            "severity": "warning",
            "summary": "Missing verdict in orchestrator output",
            "root_cause": "Orchestrator returned no verdict dict",
            "recommended_action": "Inspect agent logs and LangGraph state",
        }
    extras: dict[str, object] = {
        "notify_result": final_state.get("notify_result"),
        "docker_context": final_state.get("docker_context"),
        "llm_error": final_state.get("llm_error"),
        "raw_llm": final_state.get("raw_llm"),
    }
    await insert_verdict(verdict, extras)


async def heartbeat_loop(interval_seconds: int = 60) -> None:
    _load_env()
    await init_db()

    interval = int(os.environ.get("HEARTBEAT_INTERVAL_SECONDS", str(interval_seconds)))

    while True:
        try:
            container_name = os.getenv("DEVPLANNER_CONTAINER_NAME", "devplanner-api")
            docker_log_errors = await fetch_container_errors(container_name)
            final = await asyncio.to_thread(
                run_cycle,
                {"docker_log_errors": docker_log_errors},
            )
            await _persist_cycle_result(final)
            verdict = final.get("verdict") if isinstance(final.get("verdict"), dict) else {}
            logger.info("Heartbeat cycle completed (severity=%s)", verdict.get("severity"))
        except Exception:  # noqa: BLE001
            logger.exception("Heartbeat cycle failed")

        await asyncio.sleep(interval)


def main() -> None:
    asyncio.run(heartbeat_loop())


if __name__ == "__main__":
    main()

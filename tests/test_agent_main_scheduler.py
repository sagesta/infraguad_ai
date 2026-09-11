"""Tests for the scheduled InfraGuard agent entry point and persistence path."""

from __future__ import annotations

import asyncio
import runpy
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, sentinel

import pytest

from agent import main as agent_main


class _StopLoop(Exception):
    """Stops the deliberately infinite heartbeat after one tested cycle."""


def test_load_env_targets_repository_env(monkeypatch: pytest.MonkeyPatch) -> None:
    loader = MagicMock()
    monkeypatch.setattr(agent_main, "load_dotenv", loader)

    agent_main._load_env()

    env_path = loader.call_args.args[0]
    assert isinstance(env_path, Path)
    assert env_path.name == ".env"
    assert env_path.parent == Path(agent_main.__file__).resolve().parents[1]


@pytest.mark.asyncio
async def test_persist_cycle_result_preserves_verdict_and_extras(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    insert = AsyncMock()
    monkeypatch.setattr(agent_main, "insert_verdict", insert)
    verdict = {"severity": "critical", "summary": "Database unavailable"}
    final = {
        "verdict": verdict,
        "notify_result": {"sent": True},
        "docker_context": "container exited",
        "llm_error": None,
        "raw_llm": "raw",
        "llm_mode": "langchain",
    }

    await agent_main._persist_cycle_result(final)

    insert.assert_awaited_once_with(
        verdict,
        {
            "notify_result": {"sent": True},
            "docker_context": "container exited",
            "llm_error": None,
            "raw_llm": "raw",
            "llm_mode": "langchain",
        },
    )


@pytest.mark.asyncio
async def test_persist_cycle_result_supplies_safe_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    insert = AsyncMock()
    monkeypatch.setattr(agent_main, "insert_verdict", insert)

    await agent_main._persist_cycle_result({"verdict": "invalid"})

    persisted_verdict, extras = insert.await_args.args
    assert persisted_verdict["severity"] == "high"
    assert persisted_verdict["summary"] == "Missing verdict in orchestrator output"
    assert persisted_verdict["signature"] == "pipeline:analysis-failed:agent"
    assert extras["llm_mode"] == "unknown"


def _stop_after_sleep(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    sleep = AsyncMock(side_effect=_StopLoop)
    monkeypatch.setattr(agent_main.asyncio, "sleep", sleep)
    return sleep


@pytest.mark.asyncio
async def test_heartbeat_runs_cycle_without_docker_and_uses_configured_interval(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HEARTBEAT_INTERVAL_SECONDS", "17")
    monkeypatch.setattr(agent_main, "_load_env", MagicMock())
    init_db = AsyncMock()
    monkeypatch.setattr(agent_main, "init_db", init_db)
    monkeypatch.setattr(agent_main, "docker_monitoring_enabled", lambda: False)
    fetch_logs = AsyncMock()
    monkeypatch.setattr(agent_main, "fetch_container_errors", fetch_logs)
    fetch_acks = AsyncMock(return_value=[{"fingerprint": "known"}])
    monkeypatch.setattr(agent_main, "fetch_current_ruleset_acks", fetch_acks)
    final = {"verdict": {"severity": "ok"}}
    to_thread = AsyncMock(return_value=final)
    monkeypatch.setattr(agent_main.asyncio, "to_thread", to_thread)
    persist = AsyncMock()
    monkeypatch.setattr(agent_main, "_persist_cycle_result", persist)
    sleep = _stop_after_sleep(monkeypatch)

    with pytest.raises(_StopLoop):
        await agent_main.heartbeat_loop(interval_seconds=3)

    init_db.assert_awaited_once()
    fetch_logs.assert_not_awaited()
    fetch_acks.assert_awaited_once()
    to_thread.assert_awaited_once_with(
        agent_main.run_cycle,
        {"docker_log_errors": [], "known_conditions": [{"fingerprint": "known"}]},
    )
    persist.assert_awaited_once_with(final)
    sleep.assert_awaited_once_with(17)


@pytest.mark.asyncio
async def test_heartbeat_collects_configured_container_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("HEARTBEAT_INTERVAL_SECONDS", raising=False)
    monkeypatch.setenv("DEVPLANNER_CONTAINER_NAME", " target-api ")
    monkeypatch.setattr(agent_main, "_load_env", MagicMock())
    monkeypatch.setattr(agent_main, "init_db", AsyncMock())
    monkeypatch.setattr(agent_main, "docker_monitoring_enabled", lambda: True)
    docker_errors = [{"line": "fatal database error"}]
    fetch_logs = AsyncMock(return_value=docker_errors)
    monkeypatch.setattr(agent_main, "fetch_container_errors", fetch_logs)
    monkeypatch.setattr(agent_main, "fetch_current_ruleset_acks", AsyncMock(return_value=[]))
    final = {"verdict": {"severity": "warning"}}
    to_thread = AsyncMock(return_value=final)
    monkeypatch.setattr(agent_main.asyncio, "to_thread", to_thread)
    monkeypatch.setattr(agent_main, "_persist_cycle_result", AsyncMock())
    sleep = _stop_after_sleep(monkeypatch)

    with pytest.raises(_StopLoop):
        await agent_main.heartbeat_loop(interval_seconds=9)

    fetch_logs.assert_awaited_once_with("target-api")
    assert to_thread.await_args.args[1]["docker_log_errors"] == docker_errors
    sleep.assert_awaited_once_with(9)


@pytest.mark.asyncio
async def test_heartbeat_skips_logs_when_container_name_is_blank(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEVPLANNER_CONTAINER_NAME", "   ")
    monkeypatch.setattr(agent_main, "_load_env", MagicMock())
    monkeypatch.setattr(agent_main, "init_db", AsyncMock())
    monkeypatch.setattr(agent_main, "docker_monitoring_enabled", lambda: True)
    fetch_logs = AsyncMock()
    monkeypatch.setattr(agent_main, "fetch_container_errors", fetch_logs)
    monkeypatch.setattr(agent_main, "fetch_current_ruleset_acks", AsyncMock(return_value=[]))
    monkeypatch.setattr(
        agent_main.asyncio,
        "to_thread",
        AsyncMock(return_value={"verdict": {"severity": "ok"}}),
    )
    monkeypatch.setattr(agent_main, "_persist_cycle_result", AsyncMock())
    _stop_after_sleep(monkeypatch)

    with pytest.raises(_StopLoop):
        await agent_main.heartbeat_loop()

    fetch_logs.assert_not_awaited()


@pytest.mark.asyncio
async def test_heartbeat_logs_cycle_failure_and_keeps_scheduling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(agent_main, "_load_env", MagicMock())
    monkeypatch.setattr(agent_main, "init_db", AsyncMock())
    monkeypatch.setattr(agent_main, "docker_monitoring_enabled", lambda: False)
    monkeypatch.setattr(
        agent_main,
        "fetch_current_ruleset_acks",
        AsyncMock(side_effect=RuntimeError("database unavailable")),
    )
    log_exception = MagicMock()
    monkeypatch.setattr(agent_main.logger, "exception", log_exception)
    sleep = _stop_after_sleep(monkeypatch)

    with pytest.raises(_StopLoop):
        await agent_main.heartbeat_loop(interval_seconds=5)

    log_exception.assert_called_once_with("Heartbeat cycle failed")
    sleep.assert_awaited_once_with(5)


def test_main_runs_heartbeat_coroutine(monkeypatch: pytest.MonkeyPatch) -> None:
    heartbeat = MagicMock(return_value=sentinel.heartbeat_coroutine)
    runner = MagicMock()
    monkeypatch.setattr(agent_main, "heartbeat_loop", heartbeat)
    monkeypatch.setattr(agent_main.asyncio, "run", runner)

    agent_main.main()

    heartbeat.assert_called_once_with()
    runner.assert_called_once_with(sentinel.heartbeat_coroutine)


def test_module_entry_point_invokes_asyncio_run(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = []

    def fake_run(coroutine) -> None:
        seen.append(coroutine)
        coroutine.close()

    monkeypatch.setattr(asyncio, "run", fake_run)

    runpy.run_path(str(Path(agent_main.__file__).resolve()), run_name="__main__")

    assert len(seen) == 1

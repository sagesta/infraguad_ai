"""Orchestrator behavior tests with mocked LLM and side effects."""

from __future__ import annotations

import json
from typing import Any

import pytest

from agent.orchestrator import run_cycle


def test_critical_severity_triggers_ssh_and_notify(monkeypatch: pytest.MonkeyPatch) -> None:
    pytest.importorskip("langgraph")

    monkeypatch.setattr(
        "agent.orchestrator.fetch_loki_logs",
        lambda: {"ok": True, "lines": [], "count": 0},
    )
    monkeypatch.setattr(
        "agent.orchestrator.query_prometheus",
        lambda: {"ok": True, "metrics": {}},
    )
    monkeypatch.setattr(
        "agent.orchestrator.get_docker_events",
        lambda: {"ok": True, "events": [], "flags": {"restarts": [], "unhealthy": [], "other": []}, "count": 0},
    )
    monkeypatch.setattr(
        "agent.orchestrator.probe_endpoints",
        lambda: {"ok": True, "probes": []},
    )

    verdict: dict[str, Any] = {
        "severity": "critical",
        "summary": "Simulated outage",
        "root_cause": "Unit test injects critical verdict",
        "recommended_action": "Rollback and scale up",
    }

    def fake_get_verdict(_context: str) -> dict[str, Any]:
        out = dict(verdict)
        out["ok"] = True
        out["_raw_text"] = json.dumps(verdict)
        return out

    ssh_calls = {"n": 0}
    notify_calls = {"n": 0}

    def fake_ssh(commands: list[str] | None = None) -> dict[str, Any]:
        ssh_calls["n"] += 1
        return {"ok": True, "host": "test", "results": [{"command": "df -h", "exit_code": "0", "stdout": "", "stderr": ""}]}

    def fake_notify(*args: Any, **kwargs: Any) -> dict[str, Any]:
        notify_calls["n"] += 1
        return {"ok": True, "status_code": 200}

    monkeypatch.setattr("agent.orchestrator.get_verdict", fake_get_verdict)
    monkeypatch.setattr("agent.orchestrator.execute_remote_command", fake_ssh)
    monkeypatch.setattr("agent.orchestrator.send_push_notification", fake_notify)

    final = run_cycle()

    assert final["verdict"]["severity"] == "critical"
    assert ssh_calls["n"] == 1
    assert notify_calls["n"] == 1
    assert final.get("notify_result", {}).get("ok") is True


def test_ok_severity_skips_notify(monkeypatch: pytest.MonkeyPatch) -> None:
    pytest.importorskip("langgraph")

    monkeypatch.setattr("agent.orchestrator.fetch_loki_logs", lambda: {"ok": True, "lines": [], "count": 0})
    monkeypatch.setattr("agent.orchestrator.query_prometheus", lambda: {"ok": True, "metrics": {}})
    monkeypatch.setattr(
        "agent.orchestrator.get_docker_events",
        lambda: {"ok": True, "events": [], "flags": {"restarts": [], "unhealthy": [], "other": []}, "count": 0},
    )
    monkeypatch.setattr("agent.orchestrator.probe_endpoints", lambda: {"ok": True, "probes": []})

    verdict = {
        "severity": "ok",
        "summary": "All healthy",
        "root_cause": "Synthetic ok",
        "recommended_action": "None",
    }

    def fake_get_verdict_ok(_context: str) -> dict[str, Any]:
        out = dict(verdict)
        out["ok"] = True
        out["_raw_text"] = json.dumps(verdict)
        return out

    monkeypatch.setattr("agent.orchestrator.get_verdict", fake_get_verdict_ok)

    notify_calls = {"n": 0}

    def fake_notify(*args: Any, **kwargs: Any) -> dict[str, Any]:
        notify_calls["n"] += 1
        return {"ok": True, "status_code": 200}

    monkeypatch.setattr("agent.orchestrator.send_push_notification", fake_notify)

    final = run_cycle()
    assert final["verdict"]["severity"] == "ok"
    assert notify_calls["n"] == 0
    assert final.get("notify_result") is None

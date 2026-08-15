from __future__ import annotations

import asyncio
import os
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from agent.memory import compute_fingerprint
from api import store
from api.main import app

client = TestClient(app)


def _authed() -> patch:
    """Patch session validation so requests pass AuthMiddleware."""
    return patch("api.main.validate_session_token", return_value={"sub": "admin"})


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_returns_200() -> None:
    response = client.get("/login")
    assert response.status_code == 200


def test_status_redirects_to_login_without_auth() -> None:
    # Explicitly disabling automatic redirects in TestClient
    response = client.get("/status", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/login"


def test_status_reports_stale_agent() -> None:
    old = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    row = {
        "id": 1,
        "created_at": old,
        "severity": "ok",
        "summary": "All healthy",
        "payload": {"verdict": {"severity": "ok", "summary": "All healthy"}},
    }
    with _authed(), patch("api.main.store.fetch_latest_verdict", new_callable=AsyncMock) as mock_latest:
        mock_latest.return_value = row
        response = client.get("/status", cookies={"session": "fake"})
        assert response.status_code == 200
        data = response.json()
        assert data["stale"] is True
        assert data["age_seconds"] > 3600


def test_status_fresh_verdict_not_stale() -> None:
    now = datetime.now(timezone.utc).isoformat()
    row = {
        "id": 1,
        "created_at": now,
        "severity": "ok",
        "summary": "All healthy",
        "payload": {"verdict": {"severity": "ok", "summary": "All healthy"}},
    }
    with _authed(), patch("api.main.store.fetch_latest_verdict", new_callable=AsyncMock) as mock_latest:
        mock_latest.return_value = row
        response = client.get("/status", cookies={"session": "fake"})
        assert response.status_code == 200
        assert response.json()["stale"] is False


def test_config_reports_integrations(tmp_path) -> None:
    (tmp_path / "runbook.md").write_text("A runbook.", encoding="utf-8")
    env = {
        "LOKI_URL": "http://loki:3100",
        "PROMETHEUS_URL": "",
        "RUNBOOKS_DIR": str(tmp_path),
        "CROWDSEC_API_URL": "",
        "NTFY_TOPIC": "topic",
        "ENABLE_DOCKER_MONITORING": "0",
    }
    with _authed(), patch.dict(os.environ, env):
        response = client.get("/api/config", cookies={"session": "fake"})
        assert response.status_code == 200
        data = response.json()
        integrations = data["integrations"]
        assert integrations["loki"] is True
        assert integrations["prometheus"] is False
        assert integrations["local_runbooks"] is True
        assert integrations["crowdsec"] is False
        assert integrations["ntfy_notifications"] is True
        assert integrations["docker_monitoring"] is False
        assert data["agent_mode"] in {"langchain", "direct"}
        assert data["llm_provider"] in {"gemini", "anthropic", "openai", "ollama"}
        assert isinstance(data["model"], str) and data["model"]
        # Booleans only — no secret values may appear
        assert all(isinstance(v, bool) for v in integrations.values())


def test_threats_api_scans_loki_lines() -> None:
    with _authed(), patch(
        "agent.tools.loki.fetch_loki_logs",
        return_value={"ok": True, "lines": [], "count": 0},
    ):
        response = client.get("/api/threats", cookies={"session": "fake"})
        assert response.status_code == 200
        data = response.json()
        assert data["threats_found"] is False
        assert data["log_lines_scanned"] == 0
        assert data["loki_configured"] is True


def test_threats_api_detects_brute_force() -> None:
    lines = [{"line": f"203.0.113.5 - - GET /admin HTTP/1.1 401 unauthorized attempt {i}"} for i in range(12)]
    with _authed(), patch(
        "agent.tools.loki.fetch_loki_logs",
        return_value={"ok": True, "lines": lines, "count": len(lines)},
    ):
        response = client.get("/api/threats", cookies={"session": "fake"})
        assert response.status_code == 200
        data = response.json()
        assert data["threats_found"] is True
        assert data["threats"][0]["source_ip"] == "203.0.113.5"
        assert data["log_lines_scanned"] == 12


def test_threats_apply_dry_run_without_crowdsec() -> None:
    threat = {
        "threat_type": "ssh_brute_force",
        "source_ip": "203.0.113.5",
        "count": 15,
        "description": "IP 203.0.113.5 had 15 SSH authentication failures",
    }
    with _authed(), patch.dict(os.environ, {"CROWDSEC_API_URL": ""}):
        response = client.post("/api/threats/apply", json={"threat": threat}, cookies={"session": "fake"})
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert data["mode"] == "dry-run"
        assert data["decision"]["value"] == "203.0.113.5"
        assert data["decision"]["type"] == "ban"


def test_threats_apply_rejects_missing_threat() -> None:
    with _authed():
        response = client.post("/api/threats/apply", json={}, cookies={"session": "fake"})
        assert response.status_code == 400
        assert response.json()["error"] == "missing_threat"


def test_security_headers_present_on_unauthorized_response() -> None:
    response = client.get("/api/threats")
    assert response.status_code == 401
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert "Content-Security-Policy" in response.headers


def test_login_brute_force_is_rate_limited() -> None:
    # 5/minute on POST /login — the sixth rapid attempt must get a 429.
    statuses = []
    for _ in range(6):
        response = client.post(
            "/login",
            data={"username": "wrong", "password": "wrong"},
            follow_redirects=False,
        )
        statuses.append(response.status_code)
    assert statuses[-1] == 429
    assert all(code != 429 for code in statuses[:5])


# --- Verdict memory: acknowledge / suppress ---


def test_ack_acknowledges_and_suppresses_warning(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DB_PATH", str(tmp_path / "ack.db"))
    asyncio.run(store.init_db())
    asyncio.run(store.insert_verdict({"severity": "warning", "summary": "Disk low", "signature": "prometheus:disk-low:/"}))
    fp = compute_fingerprint("prometheus:disk-low:/")
    with _authed():
        r = client.post("/api/verdicts/ack", json={"fingerprint": fp, "note": "expected"}, cookies={"session": "fake"})
        assert r.status_code == 200 and r.json()["ok"] is True
        status = client.get("/status", cookies={"session": "fake"}).json()
        assert status["acknowledged"] is True
        assert status["suppressed"] is True


def test_ack_rejects_missing_fingerprint() -> None:
    with _authed():
        r = client.post("/api/verdicts/ack", json={}, cookies={"session": "fake"})
        assert r.status_code == 400
        assert r.json()["error"] == "missing_fingerprint"


def test_ack_unknown_fingerprint_404(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DB_PATH", str(tmp_path / "ack2.db"))
    asyncio.run(store.init_db())
    with _authed():
        r = client.post("/api/verdicts/ack", json={"fingerprint": "deadbeef"}, cookies={"session": "fake"})
        assert r.status_code == 404


def test_cannot_acknowledge_critical(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DB_PATH", str(tmp_path / "ack3.db"))
    asyncio.run(store.init_db())
    asyncio.run(store.insert_verdict({"severity": "critical", "summary": "Outage", "signature": "loki:down:api"}))
    fp = compute_fingerprint("loki:down:api")
    with _authed():
        r = client.post("/api/verdicts/ack", json={"fingerprint": fp}, cookies={"session": "fake"})
        assert r.status_code == 409
        assert r.json()["error"] == "cannot_ack_severe"


def test_unack_reopens_condition(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DB_PATH", str(tmp_path / "unack.db"))
    asyncio.run(store.init_db())
    asyncio.run(store.insert_verdict({"severity": "warning", "summary": "Disk low", "signature": "prometheus:disk-low:/"}))
    fp = compute_fingerprint("prometheus:disk-low:/")
    with _authed():
        client.post("/api/verdicts/ack", json={"fingerprint": fp}, cookies={"session": "fake"})
        assert client.get("/status", cookies={"session": "fake"}).json()["suppressed"] is True
        assert any(a["fingerprint"] == fp for a in client.get("/api/acks", cookies={"session": "fake"}).json()["acks"])

        r = client.post("/api/verdicts/unack", json={"fingerprint": fp}, cookies={"session": "fake"})
        assert r.status_code == 200 and r.json()["ok"] is True
        assert client.get("/status", cookies={"session": "fake"}).json()["suppressed"] is False

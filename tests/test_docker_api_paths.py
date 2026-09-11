"""Container-diagnostics tests using a fully mocked Docker Engine client."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from docker.errors import APIError, DockerException, NotFound

from agent.tools import docker_api


def test_monitored_names_trims_and_omits_empty_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", " api, ,worker ,, db ")
    assert docker_api._monitored_names() == ["api", "worker", "db"]


def test_no_monitored_containers_disables_diagnostics(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MONITORED_CONTAINERS", raising=False)

    result = docker_api.collect_container_diagnostics()

    assert result["ok"] is True
    assert result["monitored"] == []
    assert "disabled" in result["note"]


def test_docker_client_initialisation_error_is_structured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", "api")
    monkeypatch.setattr(
        docker_api.docker,
        "from_env",
        MagicMock(side_effect=DockerException("socket unavailable")),
    )

    result = docker_api.collect_container_diagnostics()

    assert result == {
        "ok": False,
        "error": "docker_client",
        "message": "socket unavailable",
    }


def test_collects_health_stats_logs_image_and_container_inventory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", "api,worker")
    client = MagicMock()
    api = MagicMock()
    api.attrs = {
        "State": {
            "Status": "running",
            "StartedAt": "2026-08-27T10:00:00Z",
            "ExitCode": 0,
            "Health": {
                "Status": "unhealthy",
                "FailingStreak": 2,
                "Log": [{"Output": str(index)} for index in range(8)],
            },
        },
        "RestartCount": 3,
        "Config": {"Image": "example/api:1.2.3"},
    }
    api.stats.return_value = {
        "memory_stats": {"usage": 1024, "limit": 4096},
        "cpu_stats": {"cpu_usage": {"total_usage": 987}},
        "pids_stats": {"current": 7},
    }
    api.logs.return_value = b"healthy line\ninvalid:\xff"

    worker = MagicMock()
    worker.attrs = {
        "State": {"Status": "exited", "ExitCode": 1},
        "RestartCount": 0,
        "Image": "sha256:fallback-image",
    }
    worker.stats.return_value = None
    worker.logs.return_value = "plain text logs"

    client.containers.get.side_effect = [api, worker]
    client.containers.list.return_value = [
        SimpleNamespace(short_id="abc123", name="api", status="running"),
        SimpleNamespace(short_id="def456", name=None, status="exited"),
    ]
    monkeypatch.setattr(docker_api.docker, "from_env", MagicMock(return_value=client))

    result = docker_api.collect_container_diagnostics()

    assert result["ok"] is True
    api_entry, worker_entry = result["monitored"]
    assert api_entry["status"] == "running"
    assert api_entry["restart_count"] == 3
    assert api_entry["health"]["status"] == "unhealthy"
    assert len(api_entry["health"]["log"]) == 5
    assert api_entry["health"]["log"][0] == {"Output": "3"}
    assert api_entry["stats"] == {
        "memory_usage_bytes": 1024,
        "memory_limit_bytes": 4096,
        "cpu_total_usage": 987,
        "pids": 7,
    }
    assert "\ufffd" in api_entry["logs_tail"]
    assert api_entry["image"] == "example/api:1.2.3"
    assert worker_entry["stats"] == {
        "memory_usage_bytes": None,
        "memory_limit_bytes": None,
        "cpu_total_usage": None,
        "pids": None,
    }
    assert worker_entry["logs_tail"] == "plain text logs"
    assert worker_entry["image"] == "sha256:fallback-image"
    assert result["containers_list"] == [
        {"id": "abc123", "name": "api", "status": "running"},
        {"id": "def456", "name": "", "status": "exited"},
    ]
    api.logs.assert_called_once_with(tail=50, timestamps=True)
    client.close.assert_called_once_with()


def test_records_missing_container_and_api_lookup_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", "missing,denied")
    client = MagicMock()
    client.containers.get.side_effect = [NotFound("missing"), APIError("access denied")]
    client.containers.list.return_value = []
    monkeypatch.setattr(docker_api.docker, "from_env", MagicMock(return_value=client))

    result = docker_api.collect_container_diagnostics()

    assert result["monitored"][0] == {"name": "missing", "error": "not_found"}
    assert result["monitored"][1]["error"] == "api_error"
    assert "access denied" in result["monitored"][1]["message"]
    client.close.assert_called_once_with()


def test_records_stats_logs_and_inventory_errors_but_keeps_diagnostic(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", "api")
    client = MagicMock()
    container = MagicMock()
    container.attrs = None
    container.stats.side_effect = APIError("stats denied")
    container.logs.side_effect = DockerException("logs unavailable")
    client.containers.get.return_value = container
    client.containers.list.side_effect = APIError("list denied")
    monkeypatch.setattr(docker_api.docker, "from_env", MagicMock(return_value=client))

    result = docker_api.collect_container_diagnostics()

    assert result["ok"] is True
    assert result["monitored"][0]["stats_error"]
    assert result["monitored"][0]["logs_error"] == "logs unavailable"
    assert result["monitored"][0]["image"] == ""
    assert "list denied" in result["list_error"]
    client.close.assert_called_once_with()

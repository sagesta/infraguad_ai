"""Docker event stream tests with fake HTTP transports and responses."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import httpx
import pytest

from agent.tools import docker_events


def _event(
    action: str,
    name: str,
    *,
    event_type: str = "container",
    lower_case: bool = False,
    unhealthy: bool = False,
) -> dict:
    actor = {"Attributes": {"name": name}, "ID": f"id-{name}"}
    event = {
        ("type" if lower_case else "Type"): event_type,
        ("action" if lower_case else "Action"): action,
        "Actor": actor,
    }
    if unhealthy:
        event["status"] = "health_status: unhealthy"
    return event


class _FakeResponse:
    def __init__(self, chunks, error: Exception | None = None) -> None:
        self._chunks = chunks
        self._error = error

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def raise_for_status(self) -> None:
        if self._error:
            raise self._error

    def iter_bytes(self):
        yield from self._chunks


class _FakeClient:
    def __init__(self, response: _FakeResponse) -> None:
        self.response = response
        self.stream_calls = []

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def stream(self, method, url, params):
        self.stream_calls.append((method, url, params))
        return self.response


def _install_client(monkeypatch: pytest.MonkeyPatch, response: _FakeResponse):
    fake = _FakeClient(response)
    constructor = MagicMock(return_value=fake)
    monkeypatch.setattr(docker_events.httpx, "Client", constructor)
    return fake, constructor


def test_name_helpers_normalise_and_match_compose_names(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", " /api,worker ,, ")

    assert docker_events._monitored_names() == ["api", "worker"]
    assert docker_events._is_self_container("/infraguad_ai-agent-1") is True
    assert docker_events._name_matches_monitored("/api", ["api"]) is True
    assert docker_events._name_matches_monitored("api-1", ["api"]) is True
    assert docker_events._name_matches_monitored("api_1", ["api"]) is True
    assert docker_events._name_matches_monitored("database", ["api"]) is False


@pytest.mark.parametrize(
    ("etype", "action", "name", "monitored", "expected"),
    [
        ("container", "start", "infraguad-helper", ["api"], True),
        ("network", "destroy", "bridge", ["api"], False),
        ("container", "die", "infraguad_ai-api-1", ["api"], True),
        ("container", "die", "unrelated", ["api"], True),
        ("container", "die", "api-1", ["api"], False),
        ("container", "restart", "infraguad_ai-agent-1", [], True),
        ("container", "start", "api-1", ["api"], False),
    ],
)
def test_event_filtering_rules(etype, action, name, monitored, expected) -> None:
    assert docker_events._should_omit_event(etype, action, name, monitored) is expected


def test_self_container_prefix_rules_are_independently_enforced(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Use a neutral prefix so the broad InfraGuard-name filter does not return
    # first; this proves the dedicated die/restart safeguards as well.
    monkeypatch.setattr(docker_events, "_SELF_CONTAINER_PREFIXES", ("own-agent",))

    assert docker_events._should_omit_event("container", "die", "own-agent-1", []) is True
    assert docker_events._should_omit_event("container", "restart", "own-agent-1", []) is True


def test_unconfigured_monitoring_returns_benign_empty_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("MONITORED_CONTAINERS", raising=False)

    result = docker_events.get_docker_events()

    assert result["ok"] is True
    assert result["events"] == []
    assert result["count"] == 0
    assert "disabled" in result["note"]


def test_no_configured_host_or_socket_returns_no_docker(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", "api")
    monkeypatch.delenv("DOCKER_HOST", raising=False)
    monkeypatch.setattr(docker_events.os.path, "exists", lambda _path: False)

    result = docker_events.get_docker_events()

    assert result["error"] == "no_docker"


def test_unix_stream_parses_flags_filters_noise_and_skips_invalid_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", "api")
    monkeypatch.setenv("DOCKER_HOST", "unix:///tmp/docker-test.sock")
    transport = object()
    transport_ctor = MagicMock(return_value=transport)
    monkeypatch.setattr(docker_events.httpx, "HTTPTransport", transport_ctor)
    monkeypatch.setattr(docker_events.time, "time", MagicMock(side_effect=[1000, 1000]))
    included_restart = _event("restart", "api-1")
    unhealthy = _event("health_status", "api-1", unhealthy=True)
    system_event = _event("reload", "daemon", event_type="network", lower_case=True)
    chunks = [
        (json.dumps(included_restart) + "\n" + json.dumps(unhealthy)[:20]).encode(),
        (
            json.dumps(unhealthy)[20:]
            + "\nnot-json\n\n"
            + json.dumps(_event("die", "unrelated"))
            + "\n"
            + json.dumps(_event("restart", "infraguad_ai-agent-1"))
            + "\n"
            + json.dumps(system_event)
            + "\n"
        ).encode(),
    ]
    fake, client_ctor = _install_client(monkeypatch, _FakeResponse(chunks))

    result = docker_events.get_docker_events()

    assert result["ok"] is True
    assert result["count"] == 3
    assert result["flags"]["restarts"] == ["api-1:restart"]
    assert result["flags"]["unhealthy"] == ["api-1"]
    assert system_event in result["events"]
    transport_ctor.assert_called_once_with(uds="/tmp/docker-test.sock")
    client_ctor.assert_called_once_with(timeout=10.0, transport=transport)
    assert fake.stream_calls == [
        (
            "GET",
            "http://docker/v1.45/events",
            {"since": "700", "until": "1000"},
        )
    ]


def test_tcp_host_uses_http_base_without_custom_transport(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", "api")
    monkeypatch.setenv("DOCKER_HOST", "tcp://docker.example:2375")
    fake, client_ctor = _install_client(monkeypatch, _FakeResponse([b""]))

    result = docker_events.get_docker_events()

    assert result["ok"] is True
    client_ctor.assert_called_once_with(timeout=10.0, transport=None)
    assert fake.stream_calls[0][1] == "http://docker.example:2375/v1.45/events"


def test_default_unix_socket_is_used_when_present(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", "api")
    monkeypatch.delenv("DOCKER_HOST", raising=False)
    monkeypatch.setattr(docker_events.os.path, "exists", lambda path: path == "/var/run/docker.sock")
    transport_ctor = MagicMock(return_value=object())
    monkeypatch.setattr(docker_events.httpx, "HTTPTransport", transport_ctor)
    _install_client(monkeypatch, _FakeResponse([b""]))

    assert docker_events.get_docker_events()["ok"] is True
    transport_ctor.assert_called_once_with(uds="/var/run/docker.sock")


def test_event_stream_is_capped_and_returns_last_hundred(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", "api")
    monkeypatch.setenv("DOCKER_HOST", "tcp://docker:2375")
    accepted = [_event("start", f"api-{index}") for index in range(200)]
    later_chunks = [
        [_event("restart", "api-200"), _event("start", "api-201")],
        [
            _event("health_status", "api-202", unhealthy=True),
            _event("start", "api-203"),
            _event("start", "api-204"),
        ],
    ]
    chunks = [
        ("\n".join(json.dumps(event) for event in chunk) + "\n").encode()
        for chunk in [accepted, *later_chunks]
    ]
    _install_client(monkeypatch, _FakeResponse(chunks))

    result = docker_events.get_docker_events()

    assert result["count"] == 200
    assert len(result["events"]) == 100
    assert result["events"][0]["Actor"]["Attributes"]["name"] == "api-100"
    assert result["events"][-1]["Actor"]["Attributes"]["name"] == "api-199"
    assert result["flags"] == {"restarts": [], "unhealthy": [], "other": []}


def test_http_failure_is_returned_as_structured_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", "api")
    monkeypatch.setenv("DOCKER_HOST", "tcp://docker:2375")
    request = httpx.Request("GET", "http://docker:2375/v1.45/events")
    error = httpx.ConnectError("connection refused", request=request)
    _install_client(monkeypatch, _FakeResponse([], error=error))

    result = docker_events.get_docker_events()

    assert result["error"] == "http_error"
    assert "connection refused" in result["message"]


def test_unexpected_stream_failure_is_returned_as_structured_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MONITORED_CONTAINERS", "api")
    monkeypatch.setenv("DOCKER_HOST", "tcp://docker:2375")
    _install_client(monkeypatch, _FakeResponse([], error=RuntimeError("bad event payload")))

    result = docker_events.get_docker_events()

    assert result == {
        "ok": False,
        "error": "unexpected",
        "message": "bad event payload",
    }

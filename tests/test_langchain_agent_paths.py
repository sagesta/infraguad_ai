"""Focused unit tests for the LangChain multi-tool verdict path.

All model constructors and tool calls are replaced with local fakes so this
suite never needs provider credentials, network access, or telemetry services.
"""

from __future__ import annotations

import builtins
import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from agent.llm import langchain_agent


VERDICT = {
    "severity": "warning",
    "summary": "Disk pressure detected",
    "root_cause": "Log volume is consuming the root filesystem",
    "recommended_action": "Rotate old logs",
    "signature": "prometheus:disk-low:/",
}


def _configure_provider(monkeypatch: pytest.MonkeyPatch, provider: str, model: str) -> None:
    monkeypatch.setattr(langchain_agent, "llm_provider", lambda: provider)
    monkeypatch.setattr(langchain_agent, "active_model", lambda: model)


def test_build_gemini_requires_a_key(monkeypatch: pytest.MonkeyPatch) -> None:
    _configure_provider(monkeypatch, "gemini", "gemini-test")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    result = langchain_agent.build_chat_model()

    assert result == {
        "ok": False,
        "error": "missing_env",
        "message": "GEMINI_API_KEY is not set",
    }


def test_build_gemini_accepts_google_key_and_configures_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import langchain_google_genai

    _configure_provider(monkeypatch, "gemini", "gemini-test")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("GOOGLE_API_KEY", "google-test-key")
    model = object()
    constructor = MagicMock(return_value=model)
    monkeypatch.setattr(langchain_google_genai, "ChatGoogleGenerativeAI", constructor)

    assert langchain_agent.build_chat_model() is model
    constructor.assert_called_once_with(
        model="gemini-test",
        api_key="google-test-key",
        vertexai=False,
        temperature=0.2,
    )


@pytest.mark.parametrize(
    ("provider", "module_name", "dependency"),
    [
        ("gemini", "langchain_google_genai", "langchain-google-genai"),
        ("ollama", "langchain_openai", "langchain-openai"),
        ("anthropic", "langchain_anthropic", "langchain-anthropic"),
        ("openai", "langchain_openai", "langchain-openai"),
    ],
)
def test_build_model_reports_missing_optional_dependency(
    monkeypatch: pytest.MonkeyPatch,
    provider: str,
    module_name: str,
    dependency: str,
) -> None:
    _configure_provider(monkeypatch, provider, "test-model")
    monkeypatch.setenv("GEMINI_API_KEY", "key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "key")
    monkeypatch.setenv("OPENAI_API_KEY", "key")
    real_import = builtins.__import__

    def fail_selected_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == module_name:
            raise ImportError(f"{module_name} unavailable")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fail_selected_import)

    result = langchain_agent.build_chat_model()

    assert result["ok"] is False
    assert result["error"] == "missing_dependency"
    assert dependency in result["message"]


def test_build_ollama_uses_local_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    import langchain_openai

    _configure_provider(monkeypatch, "ollama", "qwen-local")
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    model = object()
    constructor = MagicMock(return_value=model)
    monkeypatch.setattr(langchain_openai, "ChatOpenAI", constructor)

    assert langchain_agent.build_chat_model() is model
    constructor.assert_called_once_with(
        model="qwen-local",
        base_url="http://ollama:11434/v1",
        api_key="ollama",
    )


def test_build_ollama_respects_base_url_override(monkeypatch: pytest.MonkeyPatch) -> None:
    import langchain_openai

    _configure_provider(monkeypatch, "ollama", "llama-local")
    monkeypatch.setenv("OLLAMA_BASE_URL", " http://localhost:11434/v1 ")
    constructor = MagicMock(return_value=object())
    monkeypatch.setattr(langchain_openai, "ChatOpenAI", constructor)

    langchain_agent.build_chat_model()

    assert constructor.call_args.kwargs["base_url"] == "http://localhost:11434/v1"


def test_build_anthropic_requires_key(monkeypatch: pytest.MonkeyPatch) -> None:
    _configure_provider(monkeypatch, "anthropic", "claude-test")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    result = langchain_agent.build_chat_model()

    assert result["error"] == "missing_env"


def test_build_anthropic_configures_token_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    import langchain_anthropic

    _configure_provider(monkeypatch, "anthropic", "claude-test")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-test-key")
    model = object()
    constructor = MagicMock(return_value=model)
    monkeypatch.setattr(langchain_anthropic, "ChatAnthropic", constructor)

    assert langchain_agent.build_chat_model() is model
    constructor.assert_called_once_with(model="claude-test", max_tokens=8192)


def test_build_openai_requires_key(monkeypatch: pytest.MonkeyPatch) -> None:
    _configure_provider(monkeypatch, "openai", "gpt-test")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = langchain_agent.build_chat_model()

    assert result["error"] == "missing_env"


def test_build_openai_uses_active_model(monkeypatch: pytest.MonkeyPatch) -> None:
    import langchain_openai

    _configure_provider(monkeypatch, "openai", "gpt-test")
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test-key")
    model = object()
    constructor = MagicMock(return_value=model)
    monkeypatch.setattr(langchain_openai, "ChatOpenAI", constructor)

    assert langchain_agent.build_chat_model() is model
    constructor.assert_called_once_with(model="gpt-test")


def test_build_unknown_provider_returns_structured_error(monkeypatch: pytest.MonkeyPatch) -> None:
    _configure_provider(monkeypatch, "unsupported", "anything")

    result = langchain_agent.build_chat_model()

    assert result["ok"] is False
    assert result["error"] == "unknown_provider"
    assert "unsupported" in result["message"]


@pytest.mark.parametrize(
    ("output", "expected"),
    [
        ([{"type": "text", "text": "answer"}], "answer"),
        ([{"type": "image", "url": "x"}], "[{'type': 'image', 'url': 'x'}]"),
        ("plain answer", "plain answer"),
        (42, "42"),
    ],
)
def test_extract_raw_text(output, expected: str) -> None:
    assert langchain_agent.extract_raw_text(output) == expected


class _FakeTool:
    def __init__(self, name: str, result: object) -> None:
        self.name = name
        self.result = result
        self.calls: list[dict[str, object]] = []

    def invoke(self, args: dict[str, object]) -> object:
        self.calls.append(args)
        return self.result


class _FakeBoundModel:
    def __init__(self, responses: list[object]) -> None:
        self.responses = iter(responses)
        self.message_snapshots: list[list[object]] = []

    def invoke(self, messages: list[object]) -> object:
        self.message_snapshots.append(list(messages))
        return next(self.responses)


class _FakeModel:
    def __init__(self, bound: _FakeBoundModel) -> None:
        self.bound = bound
        self.bound_tools = None

    def bind_tools(self, tools):
        self.bound_tools = tools
        return self.bound


def test_run_agent_executes_known_and_unknown_tools_then_parses_verdict(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    metrics = _FakeTool("metrics", {"cpu": 0.92})
    logs = _FakeTool("logs", ["disk full"])
    first = SimpleNamespace(
        content="",
        tool_calls=[
            {"name": "metrics", "args": {"window": "5m"}, "id": "call-1"},
            {"name": "unknown", "args": {}, "id": "call-2"},
            {"name": "logs", "args": {"limit": 10}, "id": "call-3"},
        ],
    )
    final = SimpleNamespace(content=json.dumps(VERDICT), tool_calls=[])
    bound = _FakeBoundModel([first, final])
    model = _FakeModel(bound)
    monkeypatch.setattr(langchain_agent, "ALL_TOOLS", [metrics, logs])
    monkeypatch.setattr(langchain_agent, "build_chat_model", lambda: model)

    result = langchain_agent.run_langchain_agent("docker event: app restarted")

    assert result["ok"] is True
    assert result["severity"] == "warning"
    assert model.bound_tools == [metrics, logs]
    assert metrics.calls == [{"window": "5m"}]
    assert logs.calls == [{"limit": 10}]
    assert "Docker events" in bound.message_snapshots[0][1].content
    tool_messages = bound.message_snapshots[1]
    assert any("Unknown tool: unknown" in message.content for message in tool_messages)


def test_run_agent_without_context_uses_general_health_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    final = SimpleNamespace(content=[{"type": "text", "text": json.dumps(VERDICT)}], tool_calls=[])
    bound = _FakeBoundModel([final])
    monkeypatch.setattr(langchain_agent, "ALL_TOOLS", [])
    monkeypatch.setattr(langchain_agent, "build_chat_model", lambda: _FakeModel(bound))

    result = langchain_agent.run_langchain_agent()

    assert result["ok"] is True
    assert "current infrastructure health" in bound.message_snapshots[0][1].content


def test_run_agent_propagates_model_configuration_error(monkeypatch: pytest.MonkeyPatch) -> None:
    expected = {"ok": False, "error": "missing_env", "message": "key missing"}
    monkeypatch.setattr(langchain_agent, "build_chat_model", lambda: expected)

    assert langchain_agent.run_langchain_agent("ctx") is expected


def test_run_agent_rejects_empty_final_output(monkeypatch: pytest.MonkeyPatch) -> None:
    bound = _FakeBoundModel([SimpleNamespace(content="", tool_calls=[])])
    monkeypatch.setattr(langchain_agent, "ALL_TOOLS", [])
    monkeypatch.setattr(langchain_agent, "build_chat_model", lambda: _FakeModel(bound))

    result = langchain_agent.run_langchain_agent()

    assert result["error"] == "empty_output"


def test_run_agent_returns_parser_error_and_logs_warning(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    bound = _FakeBoundModel([SimpleNamespace(content="not json", tool_calls=[])])
    monkeypatch.setattr(langchain_agent, "ALL_TOOLS", [])
    monkeypatch.setattr(langchain_agent, "build_chat_model", lambda: _FakeModel(bound))

    result = langchain_agent.run_langchain_agent()

    assert result["ok"] is False
    assert result["error"] == "json_decode"
    assert "Could not parse verdict" in caplog.text


def test_run_agent_converts_execution_exception_to_structured_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _BrokenModel:
        def bind_tools(self, _tools):
            raise RuntimeError("binding failed")

    monkeypatch.setattr(langchain_agent, "build_chat_model", _BrokenModel)

    result = langchain_agent.run_langchain_agent()

    assert result == {
        "ok": False,
        "error": "langchain_agent_failed",
        "message": "binding failed",
    }

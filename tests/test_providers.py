"""Tests for the multi-provider LLM layer (Gemini, Anthropic, OpenAI, Ollama)."""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agent.llm import providers
from agent.llm.schema import parse_verdict_text
from agent.memory import compute_fingerprint

VERDICT_JSON = json.dumps(
    {
        "severity": "warning",
        "summary": "Disk is filling up",
        "root_cause": "Log volume growth on /",
        "recommended_action": "Prune old logs",
        "signature": "prometheus:disk-low:/",
    }
)


def _clear_provider_env(monkeypatch) -> None:
    for name in (
        "LLM_PROVIDER",
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "GEMINI_MODEL",
        "ANTHROPIC_MODEL",
        "OPENAI_MODEL",
        "OLLAMA_MODEL",
        "OLLAMA_BASE_URL",
    ):
        monkeypatch.delenv(name, raising=False)


# --- schema.parse_verdict_text ---


def test_parse_valid_json() -> None:
    out = parse_verdict_text(VERDICT_JSON)
    assert out["ok"] is True
    assert out["severity"] == "warning"
    assert out["signature"] == "prometheus:disk-low:/"


def test_parse_fenced_json() -> None:
    out = parse_verdict_text(f"```json\n{VERDICT_JSON}\n```")
    assert out["ok"] is True and out["severity"] == "warning"


def test_parse_json_embedded_in_prose() -> None:
    out = parse_verdict_text(f"Here is my verdict:\n{VERDICT_JSON}\nHope that helps!")
    assert out["ok"] is True and out["summary"] == "Disk is filling up"


def test_parse_rejects_invalid_severity() -> None:
    out = parse_verdict_text(json.dumps({"severity": "catastrophic", "summary": "x"}))
    assert out["ok"] is False and out["error"] == "invalid_severity"


def test_parse_rejects_empty_and_garbage() -> None:
    assert parse_verdict_text("")["error"] == "empty_output"
    assert parse_verdict_text("not json at all")["error"] == "json_decode"
    assert parse_verdict_text("[1, 2, 3]")["error"] == "invalid_shape"


# --- providers dispatch / active_model ---


def test_default_provider_is_gemini(monkeypatch) -> None:
    _clear_provider_env(monkeypatch)
    assert providers.llm_provider() == "gemini"
    assert providers.active_model() == "gemini-3.6-flash"


def test_active_model_per_provider(monkeypatch) -> None:
    _clear_provider_env(monkeypatch)
    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    assert providers.active_model() == "gemini-3.6-flash"
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.5-flash")
    assert providers.active_model() == "gemini-3.5-flash"
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    assert providers.active_model() == "claude-sonnet-5"
    monkeypatch.setenv("ANTHROPIC_MODEL", "claude-haiku-4-5")
    assert providers.active_model() == "claude-haiku-4-5"
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    assert providers.active_model() == "gpt-5.1"
    monkeypatch.setenv("OPENAI_MODEL", "gpt-5-mini")
    assert providers.active_model() == "gpt-5-mini"
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    assert providers.active_model() == "llama3.1:8b"
    monkeypatch.setenv("OLLAMA_MODEL", "qwen2.5:7b")
    assert providers.active_model() == "qwen2.5:7b"


def test_unknown_provider_errors(monkeypatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "llama")
    out = providers.get_verdict("context")
    assert out["ok"] is False and out["error"] == "unknown_provider"


def test_dispatch_routes_to_selected_provider(monkeypatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    with patch("agent.llm.anthropic_client.get_verdict", return_value={"ok": True, "severity": "ok"}) as impl:
        out = providers.get_verdict("ctx")
    assert out["ok"] is True
    impl.assert_called_once_with("ctx")


# --- Gemini Developer API client ---


def test_gemini_missing_key(monkeypatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    from agent.llm.gemini_client import get_verdict

    out = get_verdict("ctx")
    assert out["ok"] is False and out["error"] == "missing_env"


def test_gemini_parses_verdict(monkeypatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    from agent.llm.gemini_client import get_verdict

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=lambda **kw: SimpleNamespace(text=VERDICT_JSON)
        )
    )
    with patch("agent.llm.gemini_client.genai.Client", return_value=fake_client) as ctor:
        out = get_verdict("ctx")
    assert out["ok"] is True and out["severity"] == "warning"
    ctor.assert_called_once_with(api_key="test-key")


def test_dispatch_routes_to_gemini(monkeypatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    with patch("agent.llm.gemini_client.get_verdict", return_value={"ok": True, "severity": "ok"}) as impl:
        out = providers.get_verdict("ctx")
    assert out["ok"] is True
    impl.assert_called_once_with("ctx")


# --- Anthropic client ---


def _anthropic_response(text: str, stop_reason: str = "end_turn"):
    return SimpleNamespace(
        stop_reason=stop_reason,
        content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=text)],
    )


def test_anthropic_missing_key(monkeypatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from agent.llm.anthropic_client import get_verdict

    out = get_verdict("ctx")
    assert out["ok"] is False and out["error"] == "missing_env"


def test_anthropic_parses_verdict(monkeypatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    from agent.llm.anthropic_client import get_verdict

    fake_client = SimpleNamespace(
        messages=SimpleNamespace(create=lambda **kw: _anthropic_response(VERDICT_JSON))
    )
    with patch("anthropic.Anthropic", return_value=fake_client):
        out = get_verdict("ctx")
    assert out["ok"] is True
    assert out["severity"] == "warning"
    assert out["signature"] == "prometheus:disk-low:/"


def test_anthropic_refusal_is_error(monkeypatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    from agent.llm.anthropic_client import get_verdict

    fake_client = SimpleNamespace(
        messages=SimpleNamespace(create=lambda **kw: _anthropic_response("", stop_reason="refusal"))
    )
    with patch("anthropic.Anthropic", return_value=fake_client):
        out = get_verdict("ctx")
    assert out["ok"] is False and out["error"] == "refusal"


# --- OpenAI client ---


def _openai_response(text: str):
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=text))])


def test_openai_missing_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    from agent.llm.openai_client import get_verdict

    out = get_verdict("ctx")
    assert out["ok"] is False and out["error"] == "missing_env"


def test_openai_parses_verdict(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    from agent.llm.openai_client import get_verdict

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=lambda **kw: _openai_response(VERDICT_JSON))
        )
    )
    with patch("openai.OpenAI", return_value=fake_client):
        out = get_verdict("ctx")
    assert out["ok"] is True and out["severity"] == "warning"


# --- Ollama client (fully self-hosted — no API key, no cloud account) ---


def test_ollama_needs_no_api_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    from agent.llm.ollama_client import get_verdict

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=lambda **kw: _openai_response(VERDICT_JSON))
        )
    )
    with patch("openai.OpenAI", return_value=fake_client) as ctor:
        out = get_verdict("ctx")
    assert out["ok"] is True and out["severity"] == "warning"
    # No account — base_url points at the local Ollama server, key is a placeholder.
    _, kwargs = ctor.call_args
    assert kwargs["base_url"] == "http://ollama:11434/v1"
    assert kwargs["api_key"]


def test_ollama_respects_base_url_override(monkeypatch) -> None:
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    from agent.llm.ollama_client import get_verdict

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=lambda **kw: _openai_response(VERDICT_JSON))
        )
    )
    with patch("openai.OpenAI", return_value=fake_client) as ctor:
        get_verdict("ctx")
    _, kwargs = ctor.call_args
    assert kwargs["base_url"] == "http://localhost:11434/v1"


def test_ollama_network_error_is_structured(monkeypatch) -> None:
    from agent.llm.ollama_client import get_verdict

    import openai

    def _raise(**kw):
        raise openai.APIConnectionError(request=SimpleNamespace())

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=_raise)))
    with patch("openai.OpenAI", return_value=fake_client):
        out = get_verdict("ctx")
    assert out["ok"] is False and out["error"] == "network_error"


def test_dispatch_routes_to_ollama(monkeypatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    with patch("agent.llm.ollama_client.get_verdict", return_value={"ok": True, "severity": "ok"}) as impl:
        out = providers.get_verdict("ctx")
    assert out["ok"] is True
    impl.assert_called_once_with("ctx")


# --- fingerprint follows the active model (ack invalidation on switch) ---


def test_fingerprint_changes_when_provider_switches(monkeypatch, tmp_path) -> None:
    from api import store

    monkeypatch.setenv("DB_PATH", str(tmp_path / "prov.db"))
    _clear_provider_env(monkeypatch)
    asyncio.run(store.init_db())

    verdict = {"severity": "warning", "summary": "Disk low", "signature": "prometheus:disk-low:/"}
    asyncio.run(store.insert_verdict(dict(verdict)))
    row_gemini = asyncio.run(store.fetch_latest_verdict())
    assert row_gemini["fingerprint"] == compute_fingerprint("prometheus:disk-low:/", model="gemini-3.6-flash")

    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    asyncio.run(store.insert_verdict(dict(verdict)))
    row_claude = asyncio.run(store.fetch_latest_verdict())
    assert row_claude["fingerprint"] == compute_fingerprint("prometheus:disk-low:/", model="claude-sonnet-5")
    assert row_claude["fingerprint"] != row_gemini["fingerprint"]

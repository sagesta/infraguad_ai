"""Provider-agnostic LLM dispatch: Gemini (default), Anthropic, OpenAI, Ollama.

Selected via ``LLM_PROVIDER`` (gemini | anthropic | openai | ollama). The
active model name also feeds the verdict-memory fingerprint, so switching
provider or model automatically re-opens previously acknowledged conditions —
by design. ``ollama`` is the fully self-hosted option: no API key, no cloud
account, model weights served from a local container.
"""

from __future__ import annotations

import os
from typing import Any

PROVIDERS = ("gemini", "anthropic", "openai", "ollama")

_DEFAULT_MODELS = {
    "gemini": "gemini-3.6-flash",
    "anthropic": "claude-sonnet-5",
    "openai": "gpt-5.1",
    "ollama": "llama3.1:8b",
}


def llm_provider() -> str:
    return os.environ.get("LLM_PROVIDER", "").strip().lower() or "gemini"


def active_model() -> str:
    """Model name for the current provider (env override or default)."""
    provider = llm_provider()
    if provider == "gemini":
        return os.environ.get("GEMINI_MODEL", "").strip() or _DEFAULT_MODELS["gemini"]
    if provider == "anthropic":
        return os.environ.get("ANTHROPIC_MODEL", "").strip() or _DEFAULT_MODELS["anthropic"]
    if provider == "openai":
        return os.environ.get("OPENAI_MODEL", "").strip() or _DEFAULT_MODELS["openai"]
    if provider == "ollama":
        return os.environ.get("OLLAMA_MODEL", "").strip() or _DEFAULT_MODELS["ollama"]
    return _DEFAULT_MODELS["gemini"]


def get_verdict(prompt: str) -> dict[str, Any]:
    """Route the single-call verdict request to the configured provider.

    Provider modules are imported lazily so an unused provider's SDK is never
    loaded (and a missing optional dependency only affects the provider that
    needs it).
    """
    provider = llm_provider()
    if provider == "gemini":
        from agent.llm.gemini_client import get_verdict as impl
    elif provider == "anthropic":
        from agent.llm.anthropic_client import get_verdict as impl
    elif provider == "openai":
        from agent.llm.openai_client import get_verdict as impl
    elif provider == "ollama":
        from agent.llm.ollama_client import get_verdict as impl
    else:
        return {
            "ok": False,
            "error": "unknown_provider",
            "message": f"LLM_PROVIDER '{provider}' is not one of {', '.join(PROVIDERS)}",
        }
    return impl(prompt)

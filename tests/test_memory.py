"""Verdict-memory: fingerprint stability/invalidation and signature fallback."""

from __future__ import annotations

from agent.memory import OK_SIGNATURE, compute_fingerprint, derive_signature_fallback


def test_fingerprint_stable_for_same_inputs() -> None:
    a = compute_fingerprint("prometheus:disk-low:/")
    b = compute_fingerprint("prometheus:disk-low:/")
    assert a == b
    assert len(a) == 64  # sha256 hex


def test_fingerprint_normalises_case_and_whitespace() -> None:
    assert compute_fingerprint("  Prometheus:Disk-Low:/  ") == compute_fingerprint("prometheus:disk-low:/")


def test_fingerprint_changes_with_signature() -> None:
    assert compute_fingerprint("loki:error-spike:api") != compute_fingerprint("loki:error-spike:web")


def test_fingerprint_changes_with_prompt_version() -> None:
    # Bumping the ruleset version must invalidate prior acknowledgements.
    assert compute_fingerprint("prometheus:disk-low:/", prompt_version="1") != compute_fingerprint(
        "prometheus:disk-low:/", prompt_version="2"
    )


def test_fingerprint_changes_with_model() -> None:
    assert compute_fingerprint("x:y:z", model="gemini-2.5-flash") != compute_fingerprint("x:y:z", model="other-model")


def test_empty_signature_falls_back_to_ok_constant() -> None:
    assert compute_fingerprint("") == compute_fingerprint(OK_SIGNATURE)


def test_signature_fallback_ok_is_constant() -> None:
    assert derive_signature_fallback("ok", "anything at all") == OK_SIGNATURE


def test_signature_fallback_is_stable_across_volatile_tokens() -> None:
    # Same condition, different timestamps/percentages/host hashes -> same signature.
    s1 = derive_signature_fallback("warning", "Disk at 91% on / at 2026-06-15T10:00:00 host a1b2c3d4e5")
    s2 = derive_signature_fallback("warning", "Disk at 73% on / at 2026-06-15T11:30:00 host f6e5d4c3b2")
    assert s1 == s2
    assert s1.startswith("warning:")


def test_signature_fallback_distinguishes_conditions() -> None:
    assert derive_signature_fallback("warning", "disk almost full") != derive_signature_fallback(
        "warning", "memory almost exhausted"
    )

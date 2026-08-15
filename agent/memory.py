"""Stateful verdict memory: stable fingerprints and signature derivation.

A verdict ``fingerprint`` deliberately combines *what* fired (the condition
``signature``) with the *ruleset version* (``PROMPT_VERSION`` + model). When
either the condition or the rules change, the fingerprint changes and any prior
operator acknowledgement stops matching — so "mark as known" can never
permanently hide a materially different finding. This is the cache-invalidation
discipline that keeps the memory safe.
"""

from __future__ import annotations

import hashlib
import re

# Bump when the verdict prompt changes materially. Acknowledgements keyed on a
# previous PROMPT_VERSION stop matching, forcing re-evaluation under new rules.
PROMPT_VERSION = "1"

# Mirrors the default in agent.llm.providers without importing provider SDKs.
DEFAULT_MODEL = "gemini-3.6-flash"

OK_SIGNATURE = "none:healthy:all"

_IP = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_HEX = re.compile(r"\b[0-9a-f]{8,}\b", re.IGNORECASE)
_NUM = re.compile(r"\d+")
_WS = re.compile(r"\s+")
_NONWORD = re.compile(r"[^a-z0-9]+")


def compute_fingerprint(
    signature: str,
    model: str = DEFAULT_MODEL,
    prompt_version: str = PROMPT_VERSION,
) -> str:
    """Stable content-plus-ruleset fingerprint for a verdict condition.

    Same (signature, prompt_version, model) → same hash. Change any one → new
    hash, which auto-expires a prior acknowledgement.
    """
    sig = (signature or "").strip().lower() or OK_SIGNATURE
    basis = f"{sig}\x1f{prompt_version}\x1f{model}"
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()


def _normalize(text: str) -> str:
    """Strip volatile tokens (IPs, hashes, numbers) so the same condition
    normalises to the same string across heartbeats."""
    t = (text or "").lower()
    t = _IP.sub("", t)
    t = _HEX.sub("", t)
    t = _NUM.sub("", t)
    t = _WS.sub(" ", t).strip()
    return t


def derive_signature_fallback(severity: str, root_cause: str = "", summary: str = "") -> str:
    """Deterministic signature for when the model does not supply one.

    Coarser than a model-supplied signature, but stable: the same severity and
    the same normalised root cause always yield the same slug.
    """
    sev = (severity or "warning").strip().lower()
    if sev == "ok":
        return OK_SIGNATURE
    basis = _normalize(root_cause) or _normalize(summary)
    slug = _NONWORD.sub("-", basis).strip("-")[:48] or "unspecified"
    return f"{sev}:{slug}"

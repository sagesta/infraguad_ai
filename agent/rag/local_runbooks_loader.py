"""Local filesystem loader — reads runbook Markdown files as LangChain Documents.

Replaces the Notion integration: runbooks live as .md files under RUNBOOKS_DIR
(mounted read-only into the API container), so indexing never leaves the host.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from langchain_core.documents import Document

logger = logging.getLogger(__name__)


def _runbooks_dir() -> Path:
    return Path(os.environ.get("RUNBOOKS_DIR", "./runbooks").strip() or "./runbooks")


def _derive_title(text: str, fallback: str) -> str:
    """Use the first Markdown heading as the title, or the filename."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def runbooks_configured() -> bool:
    """Whether at least one runbook file is present (drives the config chip)."""
    directory = _runbooks_dir()
    return directory.is_dir() and any(directory.rglob("*.md"))


def load_local_runbooks() -> list[Document]:
    """Read every .md file under RUNBOOKS_DIR into a Document.

    Returns an empty list (never raises) if the directory is missing or empty —
    the index endpoint then reports zero documents indexed, same shape as an
    unconfigured integration elsewhere in the codebase.
    """
    directory = _runbooks_dir()
    if not directory.is_dir():
        logger.warning("RUNBOOKS_DIR %s does not exist — skipping runbook load", directory)
        return []

    documents: list[Document] = []
    for path in sorted(directory.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            logger.warning("Could not read runbook %s: %s", path, exc)
            continue
        if not text:
            continue

        relative = path.relative_to(directory)
        category = relative.parent.as_posix() if relative.parent != Path(".") else ""
        title = _derive_title(text, fallback=path.stem.replace("_", " ").replace("-", " ").title())

        documents.append(Document(
            page_content=text,
            metadata={
                "source": f"file://{relative.as_posix()}",
                "title": title,
                "category": category,
            },
        ))

    logger.info("Loaded %d runbook documents from %s", len(documents), directory)
    return documents

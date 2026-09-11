"""ChromaDB vector store with a local ONNX embedder for runbook retrieval.

Embeddings run fully on-host — no cloud API, no API key. The model weights
(~80MB, all-MiniLM-L6-v2 quantized to ONNX) are fetched once on first use and
cached under the container's home directory; mount that cache dir as a volume
so redeploys don't re-download it.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

logger = logging.getLogger(__name__)

_CHROMA_DIR = "./chroma_db"
_COLLECTION_NAME = "runbooks"


class VectorIndexBuildError(RuntimeError):
    """Raised when a runbook index refresh cannot be completed."""


class _LocalEmbeddings(Embeddings):
    """Adapts Chroma's built-in ONNX embedder to the LangChain Embeddings interface."""

    def __init__(self) -> None:
        from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

        self._fn = DefaultEmbeddingFunction()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # Chroma's ONNX embedder returns NumPy scalar values. Newer Chroma
        # releases validate every scalar and reject ``numpy.float32`` even
        # though it is numerically valid, so normalise to built-in ``float``.
        return [[float(value) for value in vector] for vector in self._fn(texts)]

    def embed_query(self, text: str) -> list[float]:
        return [float(value) for value in self._fn([text])[0]]


def _get_embedding_function() -> Any:
    """Create the local embedding function (no external API calls)."""
    return _LocalEmbeddings()


def _document_id(document: Document) -> str:
    """Return a stable ID so re-indexing updates rather than duplicates a runbook.

    Local runbooks have one document per ``source`` path.  Optional chunk/page
    metadata is included for forward compatibility if runbooks are split later.
    Documents without a source fall back to a hash of their content and metadata.
    """
    source = str(document.metadata.get("source", "")).strip()
    if source:
        identity: dict[str, Any] = {"source": source}
        for key in ("chunk_id", "chunk", "page"):
            if key in document.metadata:
                identity[key] = document.metadata[key]
    else:
        identity = {
            "page_content": document.page_content,
            "metadata": document.metadata,
        }

    payload = json.dumps(
        identity,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_index(documents: list[Document]) -> int:
    """Synchronise the ChromaDB collection with the supplied documents.

    Stable document IDs make repeated refreshes idempotent.  Current documents
    are upserted before records absent from the new input are removed, so an
    embedding/upsert failure leaves the previous records available for retry.

    Args:
        documents: List of LangChain Document objects to index.

    Returns:
        Number of documents in the refreshed index.  Zero is a successful
        result that also clears any records from an earlier index.

    Raises:
        VectorIndexBuildError: If the index could not be refreshed completely.
    """
    try:
        from langchain_community.vectorstores import Chroma

        persist_dir = str(Path(_CHROMA_DIR).resolve())
        embeddings = _get_embedding_function()
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings,
            collection_name=_COLLECTION_NAME,
        )

        existing = vectorstore.get(include=[])
        existing_ids = set(existing.get("ids") or [])
        document_ids = [_document_id(document) for document in documents]

        if len(document_ids) != len(set(document_ids)):
            raise ValueError("Runbook documents contain duplicate source identities")

        if documents:
            vectorstore.add_documents(documents=documents, ids=document_ids)
        else:
            logger.warning("No documents supplied; clearing the existing runbook index")

        stale_ids = sorted(existing_ids.difference(document_ids))
        if stale_ids:
            vectorstore.delete(ids=stale_ids)

        count = len(document_ids)
        logger.info(
            "Refreshed ChromaDB index with %d documents at %s (%d stale records removed)",
            count,
            persist_dir,
            len(stale_ids),
        )
        return count

    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to build vector index: %s", exc)
        raise VectorIndexBuildError("Failed to refresh the runbook vector index") from exc


def load_index() -> Any | None:
    """Load an existing ChromaDB index.

    Returns:
        A Chroma vectorstore instance, or None if not available.
    """
    persist_dir = str(Path(_CHROMA_DIR).resolve())
    if not Path(persist_dir).exists():
        logger.warning("ChromaDB directory %s does not exist", persist_dir)
        return None

    try:
        from langchain_community.vectorstores import Chroma

        embeddings = _get_embedding_function()
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings,
            collection_name=_COLLECTION_NAME,
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to load vector index: %s", exc)
        return None


def similarity_search(query: str, k: int = 4) -> list[Document]:
    """Search the vector store for documents similar to the query.

    Args:
        query: The search query string.
        k: Number of results to return.

    Returns:
        List of matching Document objects.
    """
    store = load_index()
    if store is None:
        return []

    try:
        return store.similarity_search(query, k=k)
    except Exception as exc:  # noqa: BLE001
        logger.error("Similarity search failed: %s", exc)
        return []

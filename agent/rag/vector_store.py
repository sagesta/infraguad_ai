"""ChromaDB vector store with a local ONNX embedder for runbook retrieval.

Embeddings run fully on-host — no cloud API, no API key. The model weights
(~80MB, all-MiniLM-L6-v2 quantized to ONNX) are fetched once on first use and
cached under the container's home directory; mount that cache dir as a volume
so redeploys don't re-download it.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

logger = logging.getLogger(__name__)

_CHROMA_DIR = "./chroma_db"
_COLLECTION_NAME = "runbooks"


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


def build_index(documents: list[Document]) -> int:
    """Build or rebuild the ChromaDB index from documents.

    Args:
        documents: List of LangChain Document objects to index.

    Returns:
        Number of documents indexed.
    """
    if not documents:
        logger.warning("No documents to index")
        return 0

    try:
        from langchain_community.vectorstores import Chroma

        persist_dir = str(Path(_CHROMA_DIR).resolve())
        embeddings = _get_embedding_function()

        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=persist_dir,
            collection_name=_COLLECTION_NAME,
        )

        count = len(documents)
        logger.info("Indexed %d documents into ChromaDB at %s", count, persist_dir)
        return count

    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to build vector index: %s", exc)
        return 0


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

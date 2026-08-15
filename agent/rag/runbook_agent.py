"""RAG runbook agent — retriever → prompt → configured LLM provider."""

from __future__ import annotations

import logging
from typing import Any

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from agent.llm.langchain_agent import build_chat_model
from agent.rag.vector_store import similarity_search

logger = logging.getLogger(__name__)

_RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an on-call assistant for infrastructure operations. "
        "Answer the question based ONLY on the runbooks provided below. "
        "If the runbooks don't contain relevant information, say so clearly. "
        "Be concise and actionable."
    )),
    ("human", (
        "RUNBOOK CONTEXT:\n{context}\n\n"
        "QUESTION: {question}"
    )),
])


def _format_docs(docs: list[Document]) -> str:
    """Format retrieved documents into a context string."""
    parts: list[str] = []
    for i, doc in enumerate(docs, 1):
        title = doc.metadata.get("title", "Untitled")
        parts.append(f"--- Runbook {i}: {title} ---\n{doc.page_content}")
    return "\n\n".join(parts) if parts else "No runbooks found."


def query_runbooks(question: str) -> dict[str, Any]:
    """Query the runbook knowledge base using RAG.

    Args:
        question: The user's question about infrastructure operations.

    Returns:
        Dict with answer text and source document titles.
    """
    try:
        # Retrieve relevant documents
        docs = similarity_search(question, k=4)

        if not docs:
            return {
                "ok": True,
                "answer": "No runbooks have been indexed yet. Add Markdown files under the runbooks "
                "directory and use the /api/runbooks/index endpoint to load them.",
                "sources": [],
            }

        llm = build_chat_model()
        if isinstance(llm, dict):
            return llm

        context = _format_docs(docs)
        chain = _RAG_PROMPT | llm | StrOutputParser()
        answer = chain.invoke({"context": context, "question": question})

        sources = [
            {"title": doc.metadata.get("title", "Untitled"), "source": doc.metadata.get("source", "")}
            for doc in docs
        ]

        return {
            "ok": True,
            "answer": answer,
            "sources": sources,
        }

    except Exception as exc:  # noqa: BLE001
        logger.error("Runbook query failed: %s", exc)
        return {"ok": False, "error": "rag_failed", "message": str(exc)}

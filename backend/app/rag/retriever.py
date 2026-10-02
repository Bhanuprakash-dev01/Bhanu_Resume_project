from __future__ import annotations

from typing import List

from backend.app.rag.vector_store import DocumentChunk, knowledge_store


class Retriever:
    def retrieve(self, query: str, limit: int = 3) -> List[DocumentChunk]:
        return knowledge_store.search_documents(query, limit=limit)

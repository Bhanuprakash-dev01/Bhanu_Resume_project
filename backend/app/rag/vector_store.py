from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class DocumentChunk:
    document_id: str
    title: str
    content: str
    source: str
    category: str
    page: str = "1"
    section: str = "general"
    version: str = "v1"
    effective_date: str = "2024-01-01"
    metadata: Dict[str, Any] = field(default_factory=dict)


class SimpleKnowledgeStore:
    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = Path(base_dir or "/workspaces/Bhanu_Resume_project/data/knowledge_base")
        self.documents: List[DocumentChunk] = []
        self._seed_data()

    def _seed_data(self) -> None:
        self.documents = [
            DocumentChunk(
                document_id="POL-001",
                title="Delivery Delay Policy",
                source="policy-manual.md",
                category="delivery_policy",
                page="10",
                section="Customer support",
                version="v3",
                effective_date="2024-05-15",
                content="Customer deliveries delayed by more than 48 hours may qualify for a refund or replacement if the carrier confirms a delivery failure. Cases involving package theft or signature refusal may require human review.",
            ),
            DocumentChunk(
                document_id="POL-002",
                title="Refund Eligibility",
                source="refund-policy.md",
                category="refund_policy",
                page="2",
                section="Refund rules",
                version="v2",
                effective_date="2024-02-10",
                content="Refunds are approved only after the order is confirmed lost or undeliverable. Refunds above $200 require manager approval and a final review record.",
            ),
            DocumentChunk(
                document_id="POL-003",
                title="Customer Communication Rules",
                source="service-guidelines.md",
                category="support_policy",
                page="7",
                section="Communication",
                version="v5",
                effective_date="2024-06-01",
                content="Agents must disclose known facts, clearly state data sources, and avoid claiming a refund or replacement has been approved unless the action tool confirms success.",
            ),
        ]

    def add_documents(self, documents: List[DocumentChunk]) -> None:
        self.documents.extend(documents)

    def search_documents(self, query: str, category: str | None = None, limit: int = 3) -> List[DocumentChunk]:
        normalized = query.lower()
        results: List[DocumentChunk] = []
        for document in self.documents:
            if category and document.category != category:
                continue
            if normalized in document.content.lower() or normalized in document.title.lower() or normalized in document.section.lower():
                results.append(document)
        return results[:limit]


knowledge_store = SimpleKnowledgeStore()

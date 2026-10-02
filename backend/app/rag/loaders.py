from __future__ import annotations

from pathlib import Path
from typing import List


class DocumentLoader:
    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = Path(base_dir or "/workspaces/Bhanu_Resume_project/data/knowledge_base")

    def load(self) -> List[str]:
        documents: List[str] = []
        for file in sorted(self.base_dir.glob("*.md")):
            documents.append(file.read_text(encoding="utf-8"))
        return documents

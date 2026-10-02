from __future__ import annotations

from typing import List


class Chunker:
    def __init__(self, chunk_size: int = 500) -> None:
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> List[str]:
        return [text[i : i + self.chunk_size] for i in range(0, len(text), self.chunk_size) if text[i : i + self.chunk_size].strip()]

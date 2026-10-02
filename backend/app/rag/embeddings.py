from __future__ import annotations

from typing import List


class EmbeddingModel:
    def __init__(self, model_name: str = "text-embedding-3-small") -> None:
        self.model_name = model_name

    def embed(self, text: str) -> List[float]:
        return [0.1, 0.2, 0.3]

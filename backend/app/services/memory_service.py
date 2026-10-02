from __future__ import annotations

from typing import Any, Dict, List


class MemoryService:
    def __init__(self) -> None:
        self.session_store: Dict[str, List[str]] = {}

    def add_session_message(self, session_id: str, message: str) -> None:
        self.session_store.setdefault(session_id, []).append(message)

    def get_session_messages(self, session_id: str) -> List[str]:
        return self.session_store.get(session_id, [])

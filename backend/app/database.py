from __future__ import annotations

from typing import Any, Dict


class DatabaseService:
    def __init__(self) -> None:
        self.connection: Dict[str, Any] = {}

    def connect(self) -> Dict[str, Any]:
        return {"status": "mock_connected", "dialect": "sqlite"}

    def query(self, sql: str) -> list[dict[str, Any]]:
        return [{"sql": sql, "result": "mock"}]

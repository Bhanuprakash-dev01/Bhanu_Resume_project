from __future__ import annotations

from typing import Any, Dict


def route_after_validation(state: Dict[str, Any]) -> str:
    validation = state.get("validation_result", {})
    if validation.get("status") in {"HUMAN_REVIEW", "BLOCK"}:
        return "human_review"
    return "response"

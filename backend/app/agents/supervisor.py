from __future__ import annotations

from typing import Any, Dict


def decide_next_step(triage: Dict[str, Any], validation: Dict[str, Any]) -> str:
    if validation.get("status") == "HUMAN_REVIEW":
        return "human_review"
    if triage.get("recommended_route") == "human_review":
        return "human_review"
    return "response"

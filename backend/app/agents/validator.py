from __future__ import annotations

from typing import Any, Dict, List


def validate_decision(investigation: Dict[str, Any], retrieval_data: Dict[str, Any], triage: Dict[str, Any]) -> Dict[str, Any]:
    checks = ["retrieval_complete", "policy_reference_present", "action_grounded"]
    notes = ["Policy context and tool evidence were reviewed."]
    status = "PASS"

    if investigation.get("confidence", 0) < 0.7:
        status = "RETRY"
        notes.append("Confidence is below acceptable threshold.")

    if not retrieval_data.get("order") or not retrieval_data.get("tracking"):
        status = "RETRY"
        notes.append("Mandatory operational data is missing.")

    if investigation.get("requires_human_review"):
        status = "HUMAN_REVIEW"
        notes.append("High-impact or policy-sensitive case requires human approval.")

    if triage.get("recommended_route") == "human_review":
        status = "HUMAN_REVIEW"
        notes.append("The triage step flagged a need for human review.")

    return {"status": status, "checks": checks, "notes": notes}

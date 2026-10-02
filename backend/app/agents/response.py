from __future__ import annotations

from typing import Any, Dict, List

from backend.app.services.llm_service import llm_service


def generate_response(query: str, triage: Dict[str, Any], retrieval_data: Dict[str, Any], investigation: Dict[str, Any], validation: Dict[str, Any], citations: List[str]) -> str:
    order = retrieval_data.get("order", {})
    tracking = retrieval_data.get("tracking", {})
    customer = retrieval_data.get("customer", {})

    base = (
        f"Known facts: the order {order.get('order_id', 'unknown')} is currently {order.get('status', 'unknown')} "
        f"for customer {customer.get('name', 'unknown')}. The latest tracking note is: {tracking.get('last_update', 'No update available')}."
    )

    evidence = (
        f"Retrieved evidence: the issue is classified as {investigation.get('issue_type', 'unknown')} with confidence "
        f"{investigation.get('confidence', 0.0)}. Policy references: {', '.join(investigation.get('policy_reference', [])) or 'No direct policy citation available.'}"
    )

    next_steps = investigation.get("recommended_action", "Review the case and gather missing details.")
    approval_note = "Pending approval" if validation.get("status") == "HUMAN_REVIEW" else "No human approval required"

    prompt = (
        f"User request: {query}\n"
        f"{base}\n"
        f"{evidence}\n"
        f"Recommended next steps: {next_steps}\n"
        f"Validation status: {validation.get('status', 'PASS')}\n"
        f"Approval: {approval_note}\n"
        f"Sources: {', '.join(citations) if citations else 'No direct citations available'}"
    )

    ai_response = llm_service.generate(prompt, system_prompt="You are a grounded customer support response generator.")
    return ai_response

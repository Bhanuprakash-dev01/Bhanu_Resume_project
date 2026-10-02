from __future__ import annotations

from typing import Any, Dict, List

from backend.app.rag.vector_store import knowledge_store


def investigate(query: str, retrieval_data: Dict[str, Any], triage: Dict[str, Any]) -> Dict[str, Any]:
    order = retrieval_data.get("order", {})
    tracking = retrieval_data.get("tracking", {})
    customer = retrieval_data.get("customer", {})
    policy_docs = knowledge_store.search_documents(query, limit=2)

    delivery_status = order.get("status", "unknown")
    issue_type = "delivery_delay"
    if "refund" in query.lower():
        issue_type = "refund_request"
    if delivery_status == "not_found":
        issue_type = "missing_order_data"

    recommended_action = "Check shipment status and confirm delivery timeline."
    if issue_type == "refund_request":
        recommended_action = "Review refund eligibility against policy and request human approval if above threshold."

    evidence = [
        {"source": "order_api", "type": "order_status", "detail": f"Order {order.get('order_id', 'unknown')} is marked as {delivery_status}."},
        {"source": "tracking_api", "type": "tracking_event", "detail": tracking.get("last_update", "No tracking update available.")},
        {"source": "customer_profile", "type": "customer_tier", "detail": f"Customer {customer.get('name', 'unknown')} is on {customer.get('tier', 'standard')} tier."},
    ]

    requires_human_review = issue_type == "refund_request" or order.get("amount", 0) > 200
    policy_reference = [f"{doc.title} ({doc.source})" for doc in policy_docs]

    return {
        "issue_type": issue_type,
        "evidence": evidence,
        "policy_reference": policy_reference,
        "recommended_action": recommended_action,
        "confidence": 0.88,
        "requires_human_review": requires_human_review,
    }

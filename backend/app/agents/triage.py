from __future__ import annotations

import re
from typing import Any, Dict, List


def triage_request(query: str) -> Dict[str, Any]:
    normalized = query.lower()
    order_match = re.search(r"ord[- ]?\w+", query, re.IGNORECASE)
    customer_match = re.search(r"cust[- ]?\w+", query, re.IGNORECASE)

    intent = "delivery_issue"
    if "refund" in normalized:
        intent = "refund_request"
    elif "tracking" in normalized:
        intent = "tracking_status"
    elif "cancel" in normalized:
        intent = "cancellation_request"

    category = "delivery"
    if "refund" in normalized:
        category = "billing"

    priority = "medium"
    if "urgent" in normalized or "asap" in normalized or "today" in normalized:
        priority = "high"

    entities = {}
    if order_match:
        entities["order_id"] = order_match.group(0).upper().replace(" ", "-")
    if customer_match:
        entities["customer_id"] = customer_match.group(0).upper().replace(" ", "-")

    missing_information: List[str] = []
    if "order" not in normalized and "ord" not in normalized:
        missing_information.append("Order ID")

    confidence = 0.86 if entities else 0.64
    recommended_route = "data_retrieval"
    if "refund" in normalized and "amount" not in normalized:
        recommended_route = "human_review"

    return {
        "intent": intent,
        "category": category,
        "priority": priority,
        "entities": entities,
        "missing_information": missing_information,
        "confidence": confidence,
        "recommended_route": recommended_route,
    }

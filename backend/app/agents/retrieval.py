from __future__ import annotations

from typing import Any, Dict

from backend.app.tools.mock_tools import get_customer, get_order, get_ticket_history, get_tracking


def retrieve_data(query: str, triage: Dict[str, Any]) -> Dict[str, Any]:
    entities = triage.get("entities", {})
    order_id = entities.get("order_id", "ORD-4401")
    customer_id = entities.get("customer_id", "CUST-1782")

    order = get_order(order_id)
    customer = get_customer(customer_id)
    tracking = get_tracking(order_id)
    ticket_history = get_ticket_history(customer_id)

    return {
        "order": order,
        "customer": customer,
        "tracking": tracking,
        "ticket_history": ticket_history,
        "source": "mock_apis",
    }

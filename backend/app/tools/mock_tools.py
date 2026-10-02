from __future__ import annotations

from typing import Any, Dict, List


MOCK_CUSTOMERS = {
    "CUST-1782": {"customer_id": "CUST-1782", "name": "Harper Lee", "tier": "gold", "email": "harper@example.com"},
    "CUST-9013": {"customer_id": "CUST-9013", "name": "Marcus Chen", "tier": "silver", "email": "marcus@example.com"},
}

MOCK_ORDERS = {
    "ORD-4401": {"order_id": "ORD-4401", "customer_id": "CUST-1782", "status": "In Transit", "amount": 189.99, "carrier": "NorthStar"},
    "ORD-9987": {"order_id": "ORD-9987", "customer_id": "CUST-9013", "status": "Delayed", "amount": 423.40, "carrier": "GridParcel"},
}

MOCK_TRACKING = {
    "ORD-4401": {"tracking_number": "NS-4508891", "expected_delivery": "2026-10-05", "last_update": "Package left local hub."},
    "ORD-9987": {"tracking_number": "GP-7701", "expected_delivery": "2026-10-02", "last_update": "Weather delay in transit."},
}

MOCK_TICKETS = {
    "CUST-1782": [{"ticket_id": "TKT-1002", "status": "open", "summary": "Late delivery inquiry"}],
    "CUST-9013": [{"ticket_id": "TKT-1108", "status": "open", "summary": "Delivery delay and refund request"}],
}


def get_customer(customer_id: str) -> Dict[str, Any]:
    return MOCK_CUSTOMERS.get(customer_id, {"customer_id": customer_id, "name": "Unknown"})


def get_order(order_id: str) -> Dict[str, Any]:
    return MOCK_ORDERS.get(order_id, {"order_id": order_id, "status": "not_found"})


def get_tracking(order_id: str) -> Dict[str, Any]:
    return MOCK_TRACKING.get(order_id, {"tracking_number": "N/A", "expected_delivery": "unknown", "last_update": "No tracking found."})


def get_ticket_history(customer_id: str) -> List[Dict[str, Any]]:
    return MOCK_TICKETS.get(customer_id, [])


def create_ticket(summary: str, order_id: str) -> Dict[str, Any]:
    return {"status": "created", "ticket_id": "TKT-AUTO-01", "summary": summary, "order_id": order_id}


def request_refund(order_id: str, amount: float) -> Dict[str, Any]:
    if amount > 200:
        return {"status": "pending_human_approval", "reason": "High-value refund requires managerial approval."}
    return {"status": "approved", "order_id": order_id, "amount": amount}


def send_notification(customer_id: str, message: str) -> Dict[str, Any]:
    return {"status": "sent", "customer_id": customer_id, "message": message}

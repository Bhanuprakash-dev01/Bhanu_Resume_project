from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_endpoint():
    response = client.post(
        "/api/chat",
        json={
            "query": "My order ORD-4401 is delayed and I want a refund.",
            "session_id": "session-001",
            "user_id": "user-001",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["workflow_id"].startswith("wf-")
    assert payload["status"] in {"running", "requires_human_review", "completed"}


def test_approval_flow():
    workflow = client.post(
        "/api/chat",
        json={
            "query": "My order ORD-4401 is delayed and I want a refund.",
            "session_id": "session-002",
            "user_id": "user-002",
        },
    ).json()

    response = client.post(
        f"/api/approval/{workflow['workflow_id']}",
        json={"workflow_id": workflow["workflow_id"], "decision": "approve", "comments": "Reviewed and approved."},
    )
    assert response.status_code == 200
    assert response.json()["human_approval"]["decision"] == "approve"

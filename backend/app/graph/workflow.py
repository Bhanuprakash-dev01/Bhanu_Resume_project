from __future__ import annotations

import uuid
from typing import Any, Dict, List

from backend.app.agents.investigation import investigate
from backend.app.agents.retrieval import retrieve_data
from backend.app.agents.response import generate_response
from backend.app.agents.supervisor import decide_next_step
from backend.app.agents.triage import triage_request
from backend.app.agents.validator import validate_decision
from backend.app.rag.vector_store import knowledge_store


def create_workflow(session_id: str, user_id: str, user_query: str) -> Dict[str, Any]:
    workflow_id = f"wf-{uuid.uuid4().hex[:8]}"
    state: Dict[str, Any] = {
        "workflow_id": workflow_id,
        "session_id": session_id,
        "user_id": user_id,
        "user_query": user_query,
        "conversation_history": [user_query],
        "current_stage": "triage",
        "status": "running",
        "confidence": 0.0,
        "errors": [],
        "intent": {},
        "entities": {},
        "retrieved_data": {},
        "retrieved_documents": [],
        "investigation_result": {},
        "proposed_actions": [],
        "tool_results": [],
        "validation_result": {},
        "human_approval": {},
        "citations": [],
        "final_response": "",
    }

    triage = triage_request(user_query)
    state["intent"] = triage
    state["entities"] = triage.get("entities", {})
    state["confidence"] = triage.get("confidence", 0.0)
    state["current_stage"] = "retrieval"

    retrieval = retrieve_data(user_query, triage)
    state["retrieved_data"] = retrieval
    state["tool_results"] = [{"source": "tool", "output": retrieval}]

    policy_docs = knowledge_store.search_documents(user_query, limit=2)
    state["retrieved_documents"] = [
        {
            "document_id": doc.document_id,
            "title": doc.title,
            "source": doc.source,
            "category": doc.category,
            "section": doc.section,
            "page": doc.page,
            "content": doc.content,
        }
        for doc in policy_docs
    ]

    investigation = investigate(user_query, retrieval, triage)
    state["investigation_result"] = investigation
    state["current_stage"] = "validation"

    validation = validate_decision(investigation, retrieval, triage)
    state["validation_result"] = validation

    citations = [
        f"{doc['title']} ({doc['source']}, section {doc['section']})"
        for doc in state["retrieved_documents"]
    ]
    state["citations"] = citations

    next_step = decide_next_step(triage, validation)
    if next_step == "human_review":
        state["current_stage"] = "human_review"
        state["status"] = "requires_human_review"
        state["proposed_actions"] = [{
            "action": "request_refund",
            "status": "pending",
            "reason": investigation.get("recommended_action", "Review policy before approving"),
        }]
        state["human_approval"] = {"required": True, "decision": "pending"}
        state["final_response"] = (
            "The case requires human approval before a refund or other consequential action is executed."
        )
        return state

    state["current_stage"] = "response"
    state["status"] = "completed"
    state["final_response"] = generate_response(
        user_query,
        triage,
        retrieval,
        investigation,
        validation,
        citations,
    )
    return state

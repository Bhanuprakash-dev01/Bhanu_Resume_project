from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import settings
from backend.app.graph.workflow import create_workflow
from backend.app.models.schemas import ApprovalRequest, ChatRequest, DocumentUploadResult, WorkflowSummary

app = FastAPI(title="Delivery Support Resolution Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WORKFLOW_STORE: Dict[str, Dict[str, Any]] = {}
SESSION_STORE: Dict[str, Dict[str, Any]] = {}


@app.get("/api/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "service": settings.app_name, "environment": settings.app_env}


@app.get("/api/metrics")
def metrics() -> Dict[str, Any]:
    return {
        "total_workflows": len(WORKFLOW_STORE),
        "total_sessions": len(SESSION_STORE),
        "status": "ok",
    }


@app.post("/api/chat")
def chat(request: ChatRequest) -> Dict[str, Any]:
    workflow = create_workflow(request.session_id, request.user_id, request.query)
    WORKFLOW_STORE[workflow["workflow_id"]] = workflow
    SESSION_STORE.setdefault(request.session_id, {"session_id": request.session_id, "messages": []})
    SESSION_STORE[request.session_id]["messages"].append({"role": "user", "content": request.query})
    SESSION_STORE[request.session_id]["messages"].append({"role": "assistant", "content": workflow["final_response"]})
    return workflow


@app.post("/api/agent/run")
def agent_run(request: ChatRequest) -> Dict[str, Any]:
    return chat(request)


@app.post("/api/documents/upload")
def upload_documents() -> DocumentUploadResult:
    return DocumentUploadResult(
        filename="sample_policy.md",
        status="uploaded",
        message="Document stub accepted for ingestion. In production, validate file type and parse content here.",
    )


@app.post("/api/documents/ingest")
def ingest_documents() -> Dict[str, Any]:
    return {"status": "success", "message": "Knowledge base ingestion queued for sample delivery policy documents."}


@app.get("/api/sessions/{session_id}")
def get_session(session_id: str) -> Dict[str, Any]:
    session = SESSION_STORE.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.get("/api/workflows/{workflow_id}")
def get_workflow(workflow_id: str) -> Dict[str, Any]:
    workflow = WORKFLOW_STORE.get(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@app.post("/api/approval/{workflow_id}")
def handle_approval(workflow_id: str, approval: ApprovalRequest) -> Dict[str, Any]:
    if approval.workflow_id != workflow_id:
        raise HTTPException(status_code=400, detail="Workflow ID mismatch")

    workflow = WORKFLOW_STORE.get(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow["human_approval"] = {"decision": approval.decision, "comments": approval.comments or ""}
    workflow["status"] = "completed"
    workflow["current_stage"] = "response"
    workflow["final_response"] = (
        "Human approval received. The recommended action has been accepted and the workflow can continue."
        if approval.decision == "approve"
        else "The request was not approved. The case remains in review until the issue is re-evaluated."
    )
    return workflow


@app.get("/")
def root() -> Dict[str, Any]:
    return {"message": "Delivery Support Resolution Agent API is running."}

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Customer issue or inquiry")
    session_id: str = Field(default="session-default")
    user_id: str = Field(default="user-default")


class ApprovalRequest(BaseModel):
    workflow_id: str
    decision: Literal["approve", "reject", "modify"]
    comments: Optional[str] = None


class TriageDecision(BaseModel):
    intent: str
    category: str
    priority: str
    entities: Dict[str, Any] = Field(default_factory=dict)
    missing_information: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    recommended_route: str


class EvidenceItem(BaseModel):
    source: str
    type: str
    detail: str


class InvestigationDecision(BaseModel):
    issue_type: str
    evidence: List[EvidenceItem] = Field(default_factory=list)
    policy_reference: List[str] = Field(default_factory=list)
    recommended_action: str
    confidence: float = 0.0
    requires_human_review: bool = False


class ValidationResult(BaseModel):
    status: Literal["PASS", "RETRY", "HUMAN_REVIEW", "BLOCK"]
    checks: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class DocumentUploadResult(BaseModel):
    filename: str
    status: str
    message: str


class WorkflowSummary(BaseModel):
    workflow_id: str
    session_id: str
    status: str
    current_stage: str
    confidence: float
    final_response: Optional[str] = None


class AgentRunResult(BaseModel):
    workflow_id: str
    status: str
    current_stage: str
    final_response: str
    confidence: float
    citations: List[str] = Field(default_factory=list)
    validation: Optional[ValidationResult] = None

from __future__ import annotations

from typing import Any, Dict


def triage_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state["current_stage"] = "triage"
    return state


def retrieval_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state["current_stage"] = "retrieval"
    return state


def investigation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state["current_stage"] = "investigation"
    return state


def validation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state["current_stage"] = "validation"
    return state


def response_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state["current_stage"] = "response"
    return state

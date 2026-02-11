"""
Loading, empty, error, and offline response contract for inspection API flows (constitution §6).
Response shapes align with OpenAPI; document in contracts/openapi.yaml.
"""
from __future__ import annotations

from typing import Any


def loading_response(step_id: str | None = None) -> dict[str, Any]:
    """Client can show loading state. Optional stepId for which step is loading."""
    return {"state": "loading", "stepId": step_id}


def empty_response(
    session_id: str,
    message: str = "No content yet",
) -> dict[str, Any]:
    """Empty state (e.g. no steps, no record)."""
    return {
        "state": "empty",
        "sessionId": session_id,
        "message": message,
    }


def error_state_response(
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Explicit error state for client (e.g. validation, not found)."""
    out: dict[str, Any] = {"state": "error", "code": code, "message": message}
    if details:
        out["details"] = details
    return out


def offline_response(
    session_id: str | None = None,
    message: str = "Offline or unavailable; retry when connected.",
) -> dict[str, Any]:
    """Offline / service unavailable."""
    out: dict[str, Any] = {"state": "offline", "message": message}
    if session_id:
        out["sessionId"] = session_id
    return out


def success_response(data: dict[str, Any]) -> dict[str, Any]:
    """Wrap successful payload (state = success)."""
    return {"state": "success", "data": data}

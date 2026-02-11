"""
Inspection session handlers: create session, get session, complete session (T027, T028, T065).
"""
from __future__ import annotations

import uuid
from datetime import datetime

from api.middleware.auth import get_tenant_id_from_path, get_user_id, require_tenant_and_user
from api.middleware.errors import error_response, not_found_response, forbidden_response
from api.middleware.response_states import error_state_response, success_response
from api.routes.router import parse_json_body
from infrastructure.config.factories import build_config
from infrastructure.persistence import session_repository, step_repository
from model.aggregates.inspection_session import InspectionSession, SessionStatus
from model.entities.intent import Intent
from model.entities.step import Step, StepSource, StepStatus
from model.entities.target import Target
from ai.graph.inspection_graph import run_initial_graph


def _parse_path_session_id(request) -> str | None:
    """Extract sessionId from path /api/v1/tenants/{tenantId}/inspection_sessions/{sessionId}."""
    path = getattr(request, "path", "") or ""
    parts = path.strip("/").split("/")
    if "inspection_sessions" in parts:
        idx = parts.index("inspection_sessions")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return None


def _is_create_path(path: str) -> bool:
    """Path is .../inspection_sessions with no session id after."""
    return path.rstrip("/").endswith("inspection_sessions")


def _is_complete_path(path: str) -> bool:
    return "complete" in path


def handle_sessions_request(request):
    """Dispatch to create_session, get_session, or complete_session by method and path."""
    path = getattr(request, "path", "") or ""
    method = (getattr(request, "method", None) or "GET").upper()
    if method == "GET":
        return get_session(request)
    if method == "POST":
        if _is_complete_path(path):
            return complete_session(request)
        if _is_create_path(path):
            return create_session(request)
    return error_response("Not found", 404)


def create_session(request):
    """POST create session from intent (T027). Enforce config (T060); vague intent → clarify (T061)."""
    auth = require_tenant_and_user(request)
    if not auth:
        return error_response("Unauthorized", 401)
    tenant_id, user_id = auth
    # Path may be /api/v1/tenants/xxx/inspection_sessions
    path = getattr(request, "path", "")
    if "/inspection_sessions" not in path and tenant_id not in path:
        tenant_id = get_tenant_id_from_path(path) or tenant_id

    body = parse_json_body(request)
    if not body or "intent" not in body:
        return error_response("intent is required", 400)
    intent_obj = body["intent"]
    goal = (intent_obj.get("goal") or "").strip()
    if not goal:
        return error_state_response("VALIDATION", "Intent goal is required"), 400
    if len(goal) < 3:
        return error_state_response("CLARIFY", "Please describe your inspection goal in more detail."), 400

    config = build_config()
    intent = Intent(goal=goal, constraints=intent_obj.get("constraints"))
    target = None
    if body.get("target"):
        t = body["target"]
        target = Target(
            type=t.get("type", ""),
            identifier=t.get("identifier"),
            display_name=t.get("displayName"),
        )

    session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    session = InspectionSession(
        id=session_id,
        tenant_id=tenant_id,
        status=SessionStatus.CREATED,
        intent=intent,
        target=target,
        created_at=now,
        updated_at=now,
        created_by=user_id,
        completed_at=None,
        record_id=None,
    )
    session.start_progress()

    steps_list, first_prompt = run_initial_graph(goal, intent.constraints)
    session_repository.save(session)

    for i, s in enumerate(steps_list):
        step = Step(
            id=s.get("id", f"step-{i}"),
            session_id=session_id,
            order=s.get("order", i),
            type=s.get("type", "check"),
            prompt=s.get("prompt", first_prompt),
            target_id=None,
            status=StepStatus.PENDING,
            created_at=now,
            updated_at=now,
            source=StepSource.INITIAL,
        )
        step_repository.save_step(tenant_id, session_id, step)

    response_data = {
        "sessionId": session_id,
        "status": session.status.value,
        "initialSteps": [{"stepId": s.get("id"), "order": s.get("order"), "type": s.get("type"), "status": "pending"} for s in steps_list],
        "currentPrompt": {"stepId": steps_list[0]["id"] if steps_list else None, "text": first_prompt, "type": "check"},
    }
    return response_data, 201


def get_session(request):
    """GET session for resumption (T028)."""
    auth = require_tenant_and_user(request)
    if not auth:
        return error_response("Unauthorized", 401)
    tenant_id, user_id = auth
    path = getattr(request, "path", "")
    tenant_id = get_tenant_id_from_path(path) or tenant_id
    session_id = _parse_path_session_id(request)
    if not session_id:
        return not_found_response("Session"), 404
    session = session_repository.load(tenant_id, session_id)
    if not session:
        return not_found_response("Session"), 404
    steps = step_repository.load_steps(tenant_id, session_id)
    current = steps[0] if steps else None
    return {
        "sessionId": session_id,
        "status": session.status.value,
        "currentPrompt": {"stepId": current.id, "text": current.prompt, "type": current.type} if current else None,
        "progress": {"totalSteps": len(steps)},
    }, 200


def complete_session(request):
    """Complete session: only primary user (session owner) can mark complete (T065)."""
    auth = require_tenant_and_user(request)
    if not auth:
        return error_response("Unauthorized", 401)
    tenant_id, user_id = auth
    path = getattr(request, "path", "")
    tenant_id = get_tenant_id_from_path(path) or tenant_id
    session_id = _parse_path_session_id(request)
    if not session_id:
        return not_found_response("Session"), 404
    session = session_repository.load(tenant_id, session_id)
    if not session:
        return not_found_response("Session"), 404
    if session.created_by != user_id:
        return forbidden_response("Only the session owner can complete the inspection"), 403
    session.complete()
    session_repository.save(session)
    return {"sessionId": session_id, "status": session.status.value}, 200

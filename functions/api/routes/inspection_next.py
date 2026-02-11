"""
Submit answer and get next prompt (T029).
"""
from __future__ import annotations

from datetime import datetime
import uuid

from api.middleware.auth import get_tenant_id_from_path, require_tenant_and_user
from api.middleware.errors import error_response, not_found_response
from api.routes.router import parse_json_body
from api.routes.inspection_sessions import _parse_path_session_id
from infrastructure.persistence import session_repository, step_repository, observation_repository
from model.entities.observation import Observation, ObservationPriority
from model.entities.step import Step, StepStatus
from ai.graph.inspection_graph import run_next_prompt


def handle_next_request(request):
    """POST .../inspection_sessions/{sessionId}/next - submit answer, get next prompt."""
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

    body = parse_json_body(request) or {}
    answer = (body.get("answer") or body.get("observation") or "").strip()
    if not answer:
        return error_response("answer or observation is required", 400)

    steps = step_repository.load_steps(tenant_id, session_id)
    if not steps:
        return {"hasNext": False, "prompt": None, "stepCompleted": None, "sessionStatus": session.status.value}, 200

    current = steps[0]
    priority = body.get("priority", "normal")
    try:
        obs_priority = ObservationPriority(priority)
    except ValueError:
        obs_priority = ObservationPriority.NORMAL

    obs = Observation(
        id=str(uuid.uuid4()),
        session_id=session_id,
        step_id=current.id,
        content=answer,
        priority=obs_priority,
        created_at=datetime.utcnow(),
        created_by=user_id,
        evidence_ids=[],
    )
    observation_repository.save_observation(tenant_id, session_id, obs)

    # Mark current step completed in DB
    current.updated_at = datetime.utcnow()
    object.__setattr__(current, "status", StepStatus.COMPLETED)
    step_repository.save_step(tenant_id, session_id, current)

    steps_dict = [{"id": s.id, "order": s.order, "type": s.type, "prompt": s.prompt, "status": s.status.value} for s in steps]
    completed_step, next_text, has_next = run_next_prompt(current.id, answer, steps_dict)

    return {
        "hasNext": has_next,
        "prompt": {"stepId": None, "text": next_text, "type": "check"} if next_text else None,
        "stepCompleted": {"stepId": completed_step["id"], "order": completed_step["order"], "type": completed_step["type"], "status": "completed"} if completed_step else None,
        "sessionStatus": session.status.value,
    }, 200

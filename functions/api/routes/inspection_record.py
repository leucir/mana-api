"""
Record generation and GET record (T031).
"""
from __future__ import annotations

from datetime import datetime

from api.middleware.auth import get_tenant_id_from_path, require_tenant_and_user
from api.middleware.errors import error_response, not_found_response
from api.routes.inspection_sessions import _parse_path_session_id
from infrastructure.persistence import (
    session_repository,
    step_repository,
    observation_repository,
    evidence_repository,
)
from model.entities.inspection_record import InspectionRecord


def _build_record(tenant_id: str, session_id: str, session) -> InspectionRecord:
    """Build InspectionRecord from session, steps, observations, evidence."""
    steps = step_repository.load_steps(tenant_id, session_id)
    findings = []
    evidence_summary = []
    incomplete = []
    follow_ups = []

    for step in steps:
        obs_list = observation_repository.load_observations_for_step(tenant_id, session_id, step.id)
        for obs in obs_list:
            findings.append({
                "stepId": step.id,
                "content": obs.content,
                "priority": obs.priority.value,
                "createdBy": obs.created_by,
                "evidenceIds": obs.evidence_ids,
            })
        if step.status.value == "pending":
            incomplete.append({"stepId": step.id, "prompt": step.prompt})

    return InspectionRecord(
        id=f"record-{session_id}",
        session_id=session_id,
        tenant_id=tenant_id,
        summary={
            "findings": findings,
            "evidenceSummary": evidence_summary,
            "incomplete": incomplete,
            "followUps": follow_ups,
        },
        generated_at=datetime.utcnow(),
        version=1,
    )


def handle_record_request(request):
    """GET .../inspection_sessions/{sessionId}/record - get decision-ready record."""
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
    if session.status.value != "completed":
        return not_found_response("Record not available until session is completed"), 404

    record = _build_record(tenant_id, session_id, session)
    return {
        "sessionId": record.session_id,
        "summary": record.summary,
        "generatedAt": record.generated_at.isoformat() + "Z",
        "version": record.version,
    }, 200

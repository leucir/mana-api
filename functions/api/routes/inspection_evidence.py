"""
Add evidence (T030).
"""
from __future__ import annotations

from datetime import datetime
import uuid

from api.middleware.auth import get_tenant_id_from_path, require_tenant_and_user
from api.middleware.errors import error_response, not_found_response, validation_error_response
from api.routes.router import parse_json_body
from api.routes.inspection_sessions import _parse_path_session_id
from infrastructure.config.factories import build_config
from infrastructure.persistence import session_repository, evidence_repository
from model.entities.evidence import Evidence, EvidenceType


def handle_evidence_request(request):
    """POST .../inspection_sessions/{sessionId}/evidence - add evidence."""
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
    observation_id = body.get("observationId")
    type_str = body.get("type", "note")
    if not observation_id:
        return validation_error_response("observationId is required"), 400
    config = build_config()
    if type_str not in config.evidence_types:
        return validation_error_response(f"type must be one of {config.evidence_types}"), 400
    try:
        evidence_type = EvidenceType(type_str)
    except ValueError:
        return validation_error_response("invalid evidence type"), 400

    storage_path = body.get("storagePath")
    payload = body.get("payload")
    if not storage_path and payload is None:
        payload = {}

    evidence_id = str(uuid.uuid4())
    evidence = Evidence(
        id=evidence_id,
        session_id=session_id,
        observation_id=observation_id,
        type=evidence_type,
        storage_path=storage_path,
        payload=payload,
        created_at=datetime.utcnow(),
        created_by=user_id,
    )
    evidence_repository.save_evidence(tenant_id, session_id, evidence)
    return {"evidenceId": evidence_id}, 201

"""
Session repository: save/load by tenantId and sessionId using Firestore client.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from infrastructure.persistence import firestore_client
from model.aggregates.inspection_session import InspectionSession, SessionStatus
from model.entities.intent import Intent
from model.entities.target import Target


def _session_to_dict(s: InspectionSession) -> dict[str, Any]:
    return {
        "id": s.id,
        "tenantId": s.tenant_id,
        "status": s.status.value,
        "intent": {"goal": s.intent.goal, "constraints": s.intent.constraints or {}},
        "target": (
            {
                "type": s.target.type,
                "identifier": s.target.identifier,
                "displayName": s.target.display_name,
            }
            if s.target
            else None
        ),
        "createdAt": s.created_at,
        "updatedAt": s.updated_at,
        "createdBy": s.created_by,
        "completedAt": s.completed_at,
        "recordId": s.record_id,
    }


def _dict_to_session(d: dict[str, Any], session_id: str) -> InspectionSession:
    intent = Intent(
        goal=d["intent"]["goal"],
        constraints=d["intent"].get("constraints"),
    )
    target = None
    if d.get("target"):
        t = d["target"]
        target = Target(
            type=t.get("type", ""),
            identifier=t.get("identifier"),
            display_name=t.get("displayName"),
        )
    return InspectionSession(
        id=session_id,
        tenant_id=d["tenantId"],
        status=SessionStatus(d.get("status", "created")),
        intent=intent,
        target=target,
        created_at=d.get("createdAt") or datetime.utcnow(),
        updated_at=d.get("updatedAt") or datetime.utcnow(),
        created_by=d["createdBy"],
        completed_at=d.get("completedAt"),
        record_id=d.get("recordId"),
    )


def save(session: InspectionSession) -> None:
    """Persist session to Firestore."""
    coll = firestore_client.firestore_session_collection(session.tenant_id)
    doc = coll.document(session.id)
    doc.set(_session_to_dict(session))


def load(tenant_id: str, session_id: str) -> InspectionSession | None:
    """Load session by tenant and session id."""
    coll = firestore_client.firestore_session_collection(tenant_id)
    doc = coll.document(session_id).get()
    if not doc.exists:
        return None
    data = doc.to_dict()
    data["id"] = doc.id
    return _dict_to_session(data, doc.id)

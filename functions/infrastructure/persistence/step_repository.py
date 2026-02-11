"""
Step persistence: subcollection under session.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from infrastructure.persistence import firestore_client
from model.entities.step import Step, StepSource, StepStatus


def _step_to_dict(s: Step) -> dict[str, Any]:
    return {
        "id": s.id,
        "sessionId": s.session_id,
        "order": s.order,
        "type": s.type,
        "prompt": s.prompt,
        "targetId": s.target_id,
        "status": s.status.value,
        "createdAt": s.created_at,
        "updatedAt": s.updated_at,
        "source": s.source.value,
    }


def _dict_to_step(d: dict[str, Any]) -> Step:
    return Step(
        id=d["id"],
        session_id=d["sessionId"],
        order=d.get("order", 0),
        type=d.get("type", "check"),
        prompt=d.get("prompt", ""),
        target_id=d.get("targetId"),
        status=StepStatus(d.get("status", "pending")),
        created_at=d.get("createdAt") or datetime.utcnow(),
        updated_at=d.get("updatedAt") or datetime.utcnow(),
        source=StepSource(d.get("source", "initial")),
    )


def save_step(tenant_id: str, session_id: str, step: Step) -> None:
    """Persist step in session subcollection."""
    coll = (
        firestore_client.firestore_session_collection(tenant_id)
        .document(session_id)
        .collection("steps")
    )
    coll.document(step.id).set(_step_to_dict(step))


def load_steps(tenant_id: str, session_id: str) -> list[Step]:
    """Load all steps for a session, ordered by order."""
    coll = (
        firestore_client.firestore_session_collection(tenant_id)
        .document(session_id)
        .collection("steps")
    )
    docs = coll.order_by("order").stream()
    return [_dict_to_step(doc.to_dict() | {"id": doc.id}) for doc in docs]

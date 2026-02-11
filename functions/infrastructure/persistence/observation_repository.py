"""
Observation persistence: subcollection under session.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from infrastructure.persistence import firestore_client
from model.entities.observation import Observation, ObservationPriority


def _obs_to_dict(o: Observation) -> dict[str, Any]:
    return {
        "id": o.id,
        "sessionId": o.session_id,
        "stepId": o.step_id,
        "content": o.content,
        "priority": o.priority.value,
        "createdAt": o.created_at,
        "createdBy": o.created_by,
        "evidenceIds": o.evidence_ids or [],
    }


def _dict_to_observation(d: dict[str, Any]) -> Observation:
    return Observation(
        id=d["id"],
        session_id=d["sessionId"],
        step_id=d["stepId"],
        content=d.get("content", ""),
        priority=ObservationPriority(d.get("priority", "normal")),
        created_at=d.get("createdAt") or datetime.utcnow(),
        created_by=d["createdBy"],
        evidence_ids=d.get("evidenceIds", []),
    )


def save_observation(tenant_id: str, session_id: str, obs: Observation) -> None:
    """Persist observation in session subcollection."""
    coll = (
        firestore_client.firestore_session_collection(tenant_id)
        .document(session_id)
        .collection("observations")
    )
    coll.document(obs.id).set(_obs_to_dict(obs))


def load_observations_for_step(tenant_id: str, session_id: str, step_id: str) -> list[Observation]:
    """Load observations for a step."""
    coll = (
        firestore_client.firestore_session_collection(tenant_id)
        .document(session_id)
        .collection("observations")
    )
    docs = coll.where("stepId", "==", step_id).stream()
    return [_dict_to_observation(doc.to_dict() | {"id": doc.id}) for doc in docs]

"""
Evidence persistence and Storage upload path (T024).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from infrastructure.persistence import firestore_client, storage_client
from model.entities.evidence import Evidence, EvidenceType


def _evidence_to_dict(e: Evidence) -> dict[str, Any]:
    return {
        "id": e.id,
        "sessionId": e.session_id,
        "observationId": e.observation_id,
        "type": e.type.value,
        "storagePath": e.storage_path,
        "payload": e.payload,
        "createdAt": e.created_at,
        "createdBy": e.created_by,
    }


def _dict_to_evidence(d: dict[str, Any]) -> Evidence:
    return Evidence(
        id=d["id"],
        session_id=d["sessionId"],
        observation_id=d["observationId"],
        type=EvidenceType(d.get("type", "note")),
        storage_path=d.get("storagePath"),
        payload=d.get("payload"),
        created_at=d.get("createdAt") or datetime.utcnow(),
        created_by=d["createdBy"],
    )


def save_evidence(tenant_id: str, session_id: str, evidence: Evidence) -> None:
    """Persist evidence metadata in session subcollection."""
    coll = (
        firestore_client.firestore_session_collection(tenant_id)
        .document(session_id)
        .collection("evidence")
    )
    coll.document(evidence.id).set(_evidence_to_dict(evidence))


def get_evidence_storage_path(tenant_id: str, session_id: str, evidence_id: str, filename: str) -> str:
    """Return Storage path for evidence file (for upload URL or client upload)."""
    return storage_client.evidence_storage_path(tenant_id, session_id, evidence_id, filename)

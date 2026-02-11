"""
Firestore client factory with tenant-scoped path pattern (data-model.md).
Path: tenants/{tenantId}/inspection_sessions/...
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from google.cloud.firestore import Client
    from google.cloud.firestore_v1 import AsyncClient

_firestore_client: "Client | None" = None


def get_firestore_client() -> "Client":
    """Return singleton Firestore client (lazy init)."""
    global _firestore_client
    if _firestore_client is None:
        from firebase_admin import firestore

        _firestore_client = firestore.client()
    return _firestore_client


def firestore_session_collection(tenant_id: str):
    """Return CollectionReference for tenants/{tenantId}/inspection_sessions."""
    client = get_firestore_client()
    return client.collection("tenants").document(tenant_id).collection("inspection_sessions")


def set_firestore_client(client: "Client | None") -> None:
    """Inject client (for tests)."""
    global _firestore_client
    _firestore_client = client

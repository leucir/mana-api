"""
Cloud Storage client factory for evidence file paths (tenant- and session-scoped).
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from google.cloud.storage.bucket import Bucket

_bucket: "Bucket | None" = None


def get_storage_bucket() -> "Bucket":
    """Return default Firebase Storage bucket (lazy init)."""
    global _bucket
    if _bucket is None:
        from firebase_admin import storage

        _bucket = storage.bucket()
    return _bucket


def evidence_storage_path(tenant_id: str, session_id: str, evidence_id: str, filename: str) -> str:
    """Build Storage path for evidence: tenants/{tenantId}/sessions/{sessionId}/evidence/{evidenceId}/{filename}."""
    return f"tenants/{tenant_id}/sessions/{session_id}/evidence/{evidence_id}/{filename}"


def set_storage_bucket(bucket: "Bucket | None") -> None:
    """Inject bucket (for tests)."""
    global _bucket
    _bucket = bucket

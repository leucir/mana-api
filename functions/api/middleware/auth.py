"""
Tenant and auth middleware: extract tenantId and user id; enforce tenant isolation.
"""
from __future__ import annotations

import re
from typing import Any

# Request-like: any object with .path and .headers (Firebase Request or Flask request)
_REQUEST = Any


def get_tenant_id_from_path(path: str) -> str | None:
    """Extract tenantId from path (e.g. /api/v1/tenants/{tenantId}/...)."""
    m = re.match(r"^/api/v1/tenants/([^/]+)", path or "")
    return m.group(1) if m else None


def get_tenant_id(request: _REQUEST) -> str | None:
    """Extract tenantId from request path."""
    path = getattr(request, "path", None) or getattr(request, "url", "") or ""
    return get_tenant_id_from_path(path)


def get_user_id(request: _REQUEST) -> str | None:
    """Extract user id from Firebase Auth token or X-User-Id header (for emulator)."""
    headers = getattr(request, "headers", {})
    uid = headers.get("X-User-Id") if hasattr(headers, "get") else None
    if uid:
        return uid
    try:
        from firebase_admin import auth

        auth_header = headers.get("Authorization", "") if hasattr(headers, "get") else ""
        token = (auth_header or "").replace("Bearer ", "").strip()
        if not token:
            return None
        decoded = auth.verify_id_token(token)
        return decoded.get("uid")
    except Exception:
        return None


def require_tenant_and_user(request: _REQUEST) -> tuple[str, str] | None:
    """
    Return (tenant_id, user_id) if both present; else None.
    Caller should return 401/403 when None.
    """
    tenant_id = get_tenant_id(request)
    user_id = get_user_id(request)
    if not tenant_id and hasattr(request, "path"):
        tenant_id = get_tenant_id_from_path(getattr(request, "path", ""))
    if tenant_id and user_id:
        return (tenant_id, user_id)
    return None

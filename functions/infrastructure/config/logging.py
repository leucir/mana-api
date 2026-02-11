"""
Structured logging with tenant isolation (constitution observability).
"""
from __future__ import annotations

import logging
import sys
from typing import Any

# Optional tenant/user context (set per request)
_tenant_id: str | None = None
_user_id: str | None = None


def set_request_context(tenant_id: str | None = None, user_id: str | None = None) -> None:
    """Set tenant/user for current request (call at entry)."""
    global _tenant_id, _user_id
    _tenant_id = tenant_id
    _user_id = user_id


def clear_request_context() -> None:
    """Clear after request."""
    set_request_context(None, None)


class TenantAdapter(logging.LoggerAdapter):
    """Inject tenant_id (and optionally user_id) into log records."""

    def process(self, msg: str, kwargs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        extra = kwargs.get("extra") or {}
        if _tenant_id is not None:
            extra["tenant_id"] = _tenant_id
        if _user_id is not None:
            extra["user_id"] = _user_id
        kwargs["extra"] = extra
        return msg, kwargs


def get_logger(name: str) -> TenantAdapter:
    """Return a logger that adds tenant (and user) to log records."""
    base = logging.getLogger(name)
    return TenantAdapter(base, {})


class TenantFormatter(logging.Formatter):
    """Format with optional tenant_id from record.extra."""

    def format(self, record: logging.LogRecord) -> str:
        tenant = getattr(record, "tenant_id", "-")
        record.tenant_id = tenant
        return super().format(record)


def configure_logging(level: str = "INFO") -> None:
    """Configure root handler with structured format."""
    fmt = "%(asctime)s %(levelname)s [%(name)s] tenant=%(tenant_id)s %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(TenantFormatter(fmt))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(level)

"""
InspectionSession aggregate (data-model.md): intent, target, status, invariants, state transitions.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from model.entities.intent import Intent
from model.entities.target import Target


class SessionStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class InspectionSession:
    """Root aggregate for an inspection session."""

    id: str
    tenant_id: str
    status: SessionStatus
    intent: Intent
    target: Target | None
    created_at: datetime
    updated_at: datetime
    created_by: str
    completed_at: datetime | None
    record_id: str | None

    def __post_init__(self) -> None:
        if not self.tenant_id or not self.created_by:
            raise ValueError("tenant_id and created_by are required")
        if self.status not in (SessionStatus.CREATED, SessionStatus.IN_PROGRESS, SessionStatus.COMPLETED):
            raise ValueError("invalid status")

    def start_progress(self) -> None:
        """Transition created → in_progress."""
        if self.status != SessionStatus.CREATED:
            raise ValueError("can only start from created")
        object.__setattr__(self, "status", SessionStatus.IN_PROGRESS)
        object.__setattr__(self, "updated_at", datetime.utcnow())

    def complete(self, record_id: str | None = None) -> None:
        """Transition to completed."""
        if self.status == SessionStatus.COMPLETED:
            return
        object.__setattr__(self, "status", SessionStatus.COMPLETED)
        object.__setattr__(self, "completed_at", datetime.utcnow())
        object.__setattr__(self, "record_id", record_id)
        object.__setattr__(self, "updated_at", datetime.utcnow())

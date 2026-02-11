"""
Step entity (data-model.md): order, type, prompt, status, source.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class StepStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class StepSource(str, Enum):
    INITIAL = "initial"
    ADDED = "added"
    BRANCHED = "branched"


@dataclass
class Step:
    """Single step in inspection flow."""

    id: str
    session_id: str
    order: int
    type: str  # check, document, micro_flow
    prompt: str
    target_id: str | None
    status: StepStatus
    created_at: datetime
    updated_at: datetime
    source: StepSource

    def __post_init__(self) -> None:
        if not self.session_id:
            raise ValueError("session_id is required")

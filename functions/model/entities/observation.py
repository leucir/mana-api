"""
Observation entity (data-model.md): content, priority, linked to step.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ObservationPriority(str, Enum):
    CRITICAL = "critical"
    NORMAL = "normal"
    LOW = "low"


@dataclass
class Observation:
    """Finding or note for a step."""

    id: str
    session_id: str
    step_id: str
    content: str
    priority: ObservationPriority
    created_at: datetime
    created_by: str
    evidence_ids: list[str]

    def __post_init__(self) -> None:
        if not self.step_id or not self.created_by:
            raise ValueError("step_id and created_by are required")

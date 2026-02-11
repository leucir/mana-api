"""
Intent value object (data-model.md): goal + constraints.
Embedded in InspectionSession.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Intent:
    """User-stated goal and optional constraints."""

    goal: str
    constraints: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if not (self.goal and self.goal.strip()):
            raise ValueError("Intent goal is required")

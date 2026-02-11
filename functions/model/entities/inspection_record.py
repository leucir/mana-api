"""
InspectionRecord value object / output type (data-model.md).
Summary with findings, evidenceSummary, incomplete, followUps.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class InspectionRecord:
    """Decision-ready record output."""

    id: str
    session_id: str
    tenant_id: str
    summary: dict[str, Any]  # findings, evidenceSummary, incomplete, followUps
    generated_at: datetime
    version: int

    def __post_init__(self) -> None:
        if not self.summary:
            raise ValueError("summary is required")
        if "findings" not in self.summary:
            self.summary.setdefault("findings", [])
        if "evidenceSummary" not in self.summary:
            self.summary.setdefault("evidenceSummary", [])
        if "incomplete" not in self.summary:
            self.summary.setdefault("incomplete", [])
        if "followUps" not in self.summary:
            self.summary.setdefault("followUps", [])

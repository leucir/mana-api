"""
Evidence entity (data-model.md): type, storagePath or payload, createdBy.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class EvidenceType(str, Enum):
    NOTE = "note"
    PHOTO = "photo"
    MEASUREMENT = "measurement"
    FILE = "file"


@dataclass
class Evidence:
    """Evidence linked to an observation."""

    id: str
    session_id: str
    observation_id: str
    type: EvidenceType
    storage_path: str | None
    payload: dict[str, Any] | None
    created_at: datetime
    created_by: str

    def __post_init__(self) -> None:
        if not self.created_by:
            raise ValueError("createdBy is required")
        if not (self.storage_path or self.payload is not None):
            raise ValueError("Either storagePath or payload must be present")

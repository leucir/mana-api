"""
Target value object (data-model.md): type, identifier, displayName.
Embedded or referenced by session.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Target:
    """Inspection target (e.g. vehicle, property)."""

    type: str
    identifier: str | None = None
    display_name: str | None = None

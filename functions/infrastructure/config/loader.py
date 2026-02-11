"""
Environment configuration loader (dev/test/prod).
Loads from env vars and optional config files per research.md.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EnvConfig:
    """Runtime environment: dev, test, or prod."""

    name: str
    google_cloud_project: str
    firestore_emulator_host: str | None
    llm_endpoint: str | None
    llm_api_key: str | None
    evidence_types: list[str]
    evidence_max_size_bytes: int
    evidence_max_count_per_observation: int
    step_libraries_enabled: list[str]
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_env(cls, env_name: str | None = None) -> "EnvConfig":
        """Build config from environment variables. env_name overrides ENV."""
        name = env_name or os.environ.get("ENV", "dev")
        return cls(
            name=name,
            google_cloud_project=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
            firestore_emulator_host=os.environ.get("FIRESTORE_EMULATOR_HOST"),
            llm_endpoint=os.environ.get("LLM_ENDPOINT"),
            llm_api_key=os.environ.get("LLM_API_KEY"),
            evidence_types=_parse_list(os.environ.get("EVIDENCE_TYPES", "note,photo,measurement,file")),
            evidence_max_size_bytes=int(os.environ.get("EVIDENCE_MAX_SIZE_BYTES", "10485760")),  # 10 MiB
            evidence_max_count_per_observation=int(
                os.environ.get("EVIDENCE_MAX_COUNT_PER_OBSERVATION", "20")
            ),
            step_libraries_enabled=_parse_list(
                os.environ.get("STEP_LIBRARIES_ENABLED", "default")
            ),
            extra={},
        )


def _parse_list(value: str) -> list[str]:
    """Parse comma-separated list from env."""
    return [s.strip() for s in value.split(",") if s.strip()]

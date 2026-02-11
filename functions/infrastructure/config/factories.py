"""
Config factory/builder for external resources (LLM, Firestore, Storage)
so tests can inject mocks.
"""
from __future__ import annotations

from typing import Any, Protocol

from infrastructure.config.loader import EnvConfig


class FirestoreClientFactory(Protocol):
    """Protocol for Firestore client factory (injectable in tests)."""

    def get_client(self): ...
    def session_collection(self, tenant_id: str): ...


class StorageClientFactory(Protocol):
    """Protocol for Storage client factory (injectable in tests)."""

    def get_bucket(self): ...
    def evidence_path(self, tenant_id: str, session_id: str, evidence_id: str, filename: str) -> str: ...


_default_firestore_factory: Any = None
_default_storage_factory: Any = None


def get_firestore_factory() -> FirestoreClientFactory:
    """Return the Firestore factory (default: real implementation)."""
    global _default_firestore_factory
    if _default_firestore_factory is None:
        from infrastructure.persistence import firestore_client

        class _Default:
            def get_client(self):
                return firestore_client.get_firestore_client()

            def session_collection(self, tenant_id: str):
                return firestore_client.firestore_session_collection(tenant_id)

        _default_firestore_factory = _Default()
    return _default_firestore_factory


def get_storage_factory() -> StorageClientFactory:
    """Return the Storage factory (default: real implementation)."""
    global _default_storage_factory
    if _default_storage_factory is None:
        from infrastructure.persistence import storage_client

        class _Default:
            def get_bucket(self):
                return storage_client.get_storage_bucket()

            def evidence_path(
                self, tenant_id: str, session_id: str, evidence_id: str, filename: str
            ) -> str:
                return storage_client.evidence_storage_path(
                    tenant_id, session_id, evidence_id, filename
                )

        _default_storage_factory = _Default()
    return _default_storage_factory


def set_firestore_factory(factory: FirestoreClientFactory | None) -> None:
    """Inject Firestore factory (for tests)."""
    global _default_firestore_factory
    _default_firestore_factory = factory


def set_storage_factory(factory: StorageClientFactory | None) -> None:
    """Inject Storage factory (for tests)."""
    global _default_storage_factory
    _default_storage_factory = factory


def build_config(env_name: str | None = None) -> EnvConfig:
    """Build EnvConfig (from loader); tests can override env_name."""
    from infrastructure.config.loader import EnvConfig

    return EnvConfig.from_env(env_name)

"""
Metrics and distributed tracing with tenant isolation (constitution §9).
Complements logging from T011 (logging.py).
"""
from __future__ import annotations

import os
from typing import Any

# Trace ID can be set from incoming header (e.g. X-Cloud-Trace-Context) or generated
_trace_id: str | None = None
_span_id: str | None = None


def set_trace_context(trace_id: str | None = None, span_id: str | None = None) -> None:
    """Set trace/span for current request."""
    global _trace_id, _span_id
    _trace_id = trace_id
    _span_id = span_id


def get_trace_id() -> str | None:
    return _trace_id


def get_span_id() -> str | None:
    return _span_id


def record_metric(
    name: str,
    value: float = 1.0,
    labels: dict[str, str] | None = None,
) -> None:
    """
    Record a metric (e.g. counter or value).
    In production, wire to Cloud Monitoring; in dev, can log.
    """
    # Optional: Google Cloud Monitoring client
    # For now, ensure logging includes metric name so it can be scraped
    from infrastructure.config.logging import get_logger

    log = get_logger("observability")
    payload: dict[str, Any] = {"metric": name, "value": value}
    if labels:
        payload["labels"] = labels
    if _trace_id:
        payload["trace_id"] = _trace_id
    log.info("metric: %s", payload)


def clear_trace_context() -> None:
    """Clear after request."""
    set_trace_context(None, None)

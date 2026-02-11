"""
Base error handling and user-friendly error responses.
"""
from __future__ import annotations

from typing import Any


def error_response(
    message: str,
    code: int = 400,
    details: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], int]:
    """Return (json_body, status_code) for API error."""
    body: dict[str, Any] = {"error": message}
    if details:
        body["details"] = details
    return body, code


def not_found_response(resource: str = "Resource") -> tuple[dict[str, Any], int]:
    """404 with user-friendly message."""
    return error_response(f"{resource} not found", 404)


def forbidden_response(message: str = "Forbidden") -> tuple[dict[str, Any], int]:
    """403 Forbidden."""
    return error_response(message, 403)


def unauthorized_response(message: str = "Unauthorized") -> tuple[dict[str, Any], int]:
    """401 Unauthorized."""
    return error_response(message, 401)


def validation_error_response(message: str, details: dict[str, Any] | None = None) -> tuple[dict[str, Any], int]:
    """400 validation error."""
    return error_response(message, 400, details)

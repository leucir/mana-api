"""
Shared request helpers. (Central dispatch removed; each Cloud Function calls its handler directly.)
"""
from __future__ import annotations

import json


def parse_json_body(request) -> dict | None:
    """Parse JSON body from Firebase Request."""
    try:
        data = request.get_json(silent=True) if hasattr(request, "get_json") else None
        if data is not None:
            return data
        raw = getattr(request, "data", None) or getattr(request, "get_data", lambda: b"")()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        return json.loads(raw) if raw else None
    except Exception:
        return None

"""
Integration test for full US1 journey (T016).
Create session → answer prompts → complete session → get record.

Runs against the Firebase Functions emulator by default (make run-functions).
Override with INSPECTION_FUNCTIONS_BASE_URL or INSPECTION_API_BASE_URL.
"""
import json
import urllib.request

import pytest

from tests.conftest import get_sessions_url, get_next_url, get_record_url, emulator_reachable


@pytest.fixture
def api_urls():
    """Base URLs for each function (sessions, next, evidence, record)."""
    sessions = get_sessions_url()
    if not sessions:
        pytest.skip("INSPECTION_FUNCTIONS_BASE_URL or INSPECTION_API_BASE_URL not set")
    return {
        "sessions": sessions,
        "next": get_next_url(),
        "record": get_record_url(),
    }


@pytest.mark.integration
def test_us1_full_flow(api_urls):
    """
    Full flow: create session → POST next (answer) → complete session → GET record.
    Fails if any step returns an error (e.g. 404 on record); 200 required on record.
    Skips if Functions emulator is not reachable (make run-functions).
    """
    if not emulator_reachable():
        pytest.skip("Firebase Functions emulator not reachable. Start with: make run-functions")

    tenant_id = "test-tenant"
    user_id = "test-user"
    headers = {"Content-Type": "application/json", "X-User-Id": user_id}

    # 1. Create session (inspection_sessions)
    req = urllib.request.Request(
        f"{api_urls['sessions']}/api/v1/tenants/{tenant_id}/inspection_sessions",
        data=json.dumps({"intent": {"goal": "Inspect vehicle"}}).encode(),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.status == 201
        create_data = json.load(resp)
        session_id = create_data.get("sessionId")
        assert session_id

    # 2. Submit answer (inspection_next)
    next_req = urllib.request.Request(
        f"{api_urls['next']}/api/v1/tenants/{tenant_id}/inspection_sessions/{session_id}/next",
        data=json.dumps({"answer": "No damage visible"}).encode(),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(next_req, timeout=5) as resp:
        assert resp.status == 200

    # 3. Complete session (POST .../complete) so record becomes available
    complete_req = urllib.request.Request(
        f"{api_urls['sessions']}/api/v1/tenants/{tenant_id}/inspection_sessions/{session_id}/complete",
        data=b"{}",
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(complete_req, timeout=5) as resp:
        assert resp.status == 200

    # 4. GET record (inspection_record) — must return 200 after complete
    record_req = urllib.request.Request(
        f"{api_urls['record']}/api/v1/tenants/{tenant_id}/inspection_sessions/{session_id}/record",
        headers=headers,
        method="GET",
    )
    with urllib.request.urlopen(record_req, timeout=5) as resp:
        assert resp.status == 200
        record_data = json.load(resp)
        assert "sessionId" in record_data
        assert record_data["sessionId"] == session_id

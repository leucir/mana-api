"""
Integration tests that run against the Firebase Functions emulator.

Requires the emulator to be running: `make run-functions` (or firebase emulators:start --only functions).
Uses default emulator URL (127.0.0.1:5001/PROJECT_ID/us-central1) unless INSPECTION_FUNCTIONS_BASE_URL is set.
"""
import json
import urllib.error
import urllib.request

import pytest

from tests.conftest import (
    get_sessions_url,
    get_next_url,
    get_evidence_url,
    get_record_url,
    emulator_reachable,
)


@pytest.fixture(scope="module")
def emulator_required():
    """Skip entire module if emulator is not reachable."""
    if not emulator_reachable():
        pytest.skip(
            "Firebase Functions emulator not reachable. Start it with: make run-functions"
        )


@pytest.fixture
def api_urls():
    return {
        "sessions": get_sessions_url(),
        "next": get_next_url(),
        "evidence": get_evidence_url(),
        "record": get_record_url(),
    }


@pytest.mark.integration
def test_emulator_create_session(emulator_required, api_urls):
    """POST create session returns 201 with sessionId and status."""
    req = urllib.request.Request(
        f"{api_urls['sessions']}/api/v1/tenants/tenant1/inspection_sessions",
        data=json.dumps({"intent": {"goal": "Inspect vehicle"}}).encode(),
        headers={"Content-Type": "application/json", "X-User-Id": "user1"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.status == 201
        data = json.load(resp)
        assert "sessionId" in data
        assert data.get("status") in ("created", "in_progress")


@pytest.mark.integration
def test_emulator_get_session_after_create(emulator_required, api_urls):
    """Create session then GET same session returns 200 with session state."""
    # Create
    req = urllib.request.Request(
        f"{api_urls['sessions']}/api/v1/tenants/tenant1/inspection_sessions",
        data=json.dumps({"intent": {"goal": "Check roof"}}).encode(),
        headers={"Content-Type": "application/json", "X-User-Id": "user1"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.load(resp)
        session_id = data["sessionId"]
    # Get
    get_req = urllib.request.Request(
        f"{api_urls['sessions']}/api/v1/tenants/tenant1/inspection_sessions/{session_id}",
        headers={"X-User-Id": "user1"},
        method="GET",
    )
    with urllib.request.urlopen(get_req, timeout=5) as get_resp:
        assert get_resp.status == 200
        get_data = json.load(get_resp)
        assert get_data.get("sessionId") == session_id
        assert "status" in get_data


@pytest.mark.integration
def test_emulator_next_after_create(emulator_required, api_urls):
    """Create session then POST next returns 200 with hasNext/sessionStatus."""
    req = urllib.request.Request(
        f"{api_urls['sessions']}/api/v1/tenants/tenant1/inspection_sessions",
        data=json.dumps({"intent": {"goal": "Inspect tyres"}}).encode(),
        headers={"Content-Type": "application/json", "X-User-Id": "user1"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        session_id = json.load(resp)["sessionId"]
    next_req = urllib.request.Request(
        f"{api_urls['next']}/api/v1/tenants/tenant1/inspection_sessions/{session_id}/next",
        data=json.dumps({"answer": "All good"}).encode(),
        headers={"Content-Type": "application/json", "X-User-Id": "user1"},
        method="POST",
    )
    with urllib.request.urlopen(next_req, timeout=5) as next_resp:
        assert next_resp.status == 200
        next_data = json.load(next_resp)
        assert "sessionStatus" in next_data


@pytest.mark.integration
def test_emulator_record_before_complete_returns_404(emulator_required, api_urls):
    """GET record before session is completed returns 404."""
    req = urllib.request.Request(
        f"{api_urls['sessions']}/api/v1/tenants/tenant1/inspection_sessions",
        data=json.dumps({"intent": {"goal": "Quick check"}}).encode(),
        headers={"Content-Type": "application/json", "X-User-Id": "user1"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        session_id = json.load(resp)["sessionId"]
    record_req = urllib.request.Request(
        f"{api_urls['record']}/api/v1/tenants/tenant1/inspection_sessions/{session_id}/record",
        headers={"X-User-Id": "user1"},
        method="GET",
    )
    try:
        urllib.request.urlopen(record_req, timeout=5)
    except urllib.error.HTTPError as e:
        assert e.code == 404, f"Expected 404, got {e.code}"
    else:
        pytest.fail("Expected GET record before complete to return 404")

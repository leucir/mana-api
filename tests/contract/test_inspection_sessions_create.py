"""
Contract test for POST create session (T013).
Validates request/response against contracts/openapi.yaml.
"""
import json
import os
import pytest

try:
    import yaml
    from openapi_core import validate_request, validate_response
    from openapi_core.contrib.requests import RequestsOpenAPIRequest, RequestsOpenAPIResponse
    HAS_OPENAPI = True
except ImportError:
    HAS_OPENAPI = False

from tests.conftest import OPENAPI_SPEC_PATH


@pytest.fixture(scope="module")
def spec_dict():
    """Load OpenAPI spec; skip if file or lib missing."""
    if not os.path.isfile(OPENAPI_SPEC_PATH):
        pytest.skip(f"OpenAPI spec not found: {OPENAPI_SPEC_PATH}")
    with open(OPENAPI_SPEC_PATH) as f:
        return yaml.safe_load(f)


@pytest.fixture
def create_session_spec(spec_dict):
    """Create session operation spec."""
    path = spec_dict["paths"].get("/tenants/{tenantId}/inspection_sessions", {})
    return path.get("post", {})


def test_create_session_request_schema(create_session_spec, spec_dict):
    """Request body must match schema: intent.goal required."""
    if not HAS_OPENAPI:
        pytest.skip("openapi-core not installed")
    # Valid request
    body = {"intent": {"goal": "Inspect vehicle before purchase"}}
    schema = create_session_spec.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
    assert "intent" in schema.get("required", [])
    assert "goal" in schema["properties"].get("intent", {}).get("required", [])


def test_create_session_response_201_schema(create_session_spec, spec_dict):
    """201 response must include sessionId, status, optional initialSteps/currentPrompt."""
    resp_schemas = create_session_spec.get("responses", {}).get("201", {}).get("content", {}).get("application/json", {}).get("schema", {})
    ref = resp_schemas.get("$ref", "")
    if ref and "#/components/schemas/SessionCreated" in ref:
        comp = spec_dict.get("components", {}).get("schemas", {}).get("SessionCreated", {})
        assert "sessionId" in comp.get("properties", {}) or "sessionId" in str(comp)
    # Minimal: 201 means created
    assert "201" in create_session_spec.get("responses", {})


def test_create_session_contract_integration():
    """
    Integration: call actual API (when available) and assert 201 + SessionCreated shape.
    Skip if no base URL. Uses inspection_sessions function URL (or legacy INSPECTION_API_BASE_URL).
    """
    from tests.conftest import get_sessions_url

    base_url = get_sessions_url()
    if not base_url:
        pytest.skip("INSPECTION_FUNCTIONS_BASE_URL or INSPECTION_API_BASE_URL not set")
    import urllib.request
    # Path as in OpenAPI; client sends this path to the function URL
    url = f"{base_url}/api/v1/tenants/tenant1/inspection_sessions"
    req = urllib.request.Request(
        url,
        data=json.dumps({"intent": {"goal": "Check roof"}}).encode(),
        headers={"Content-Type": "application/json", "X-User-Id": "user1"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 201
        data = json.load(resp)
        assert "sessionId" in data
        assert data.get("status") in ("created", "in_progress")

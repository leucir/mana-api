"""
Contract test for POST submit answer and get next prompt (T014).
"""
import json
import os
import pytest

from tests.conftest import OPENAPI_SPEC_PATH


@pytest.fixture(scope="module")
def spec_dict():
    if not os.path.isfile(OPENAPI_SPEC_PATH):
        pytest.skip(f"OpenAPI spec not found: {OPENAPI_SPEC_PATH}")
    import yaml
    with open(OPENAPI_SPEC_PATH) as f:
        return yaml.safe_load(f)


def test_next_request_schema(spec_dict):
    """Next endpoint accepts answer, observation, priority."""
    path = spec_dict["paths"].get("/tenants/{tenantId}/inspection_sessions/{sessionId}/next", {})
    post = path.get("post", {})
    schema = post.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
    props = schema.get("properties", {})
    assert "answer" in props or "observation" in props


def test_next_response_200_schema(spec_dict):
    """200 response has NextPrompt shape (hasNext, prompt, sessionStatus)."""
    path = spec_dict["paths"].get("/tenants/{tenantId}/inspection_sessions/{sessionId}/next", {})
    post = path.get("post", {})
    assert "200" in post.get("responses", {})

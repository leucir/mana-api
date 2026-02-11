"""
Contract test for POST add evidence and GET record (T015).
"""
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


def test_evidence_post_schema(spec_dict):
    """Evidence POST requires observationId, type (note|photo|measurement|file)."""
    path = spec_dict["paths"].get("/tenants/{tenantId}/inspection_sessions/{sessionId}/evidence", {})
    post = path.get("post", {})
    schema = post.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
    required = schema.get("required", [])
    assert "observationId" in required
    assert "type" in required


def test_record_get_schema(spec_dict):
    """GET record returns InspectionRecord (summary.findings, evidenceSummary, incomplete, followUps)."""
    path = spec_dict["paths"].get("/tenants/{tenantId}/inspection_sessions/{sessionId}/record", {})
    get_op = path.get("get", {})
    assert "200" in get_op.get("responses", {})

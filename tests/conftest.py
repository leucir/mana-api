"""Pytest configuration and fixtures."""
import os
import sys

# Ensure functions package is on path when running from repo root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUNCTIONS_DIR = os.path.join(REPO_ROOT, "functions")
if FUNCTIONS_DIR not in sys.path:
    sys.path.insert(0, FUNCTIONS_DIR)

# OpenAPI spec path (set OPENAPI_SPEC to main repo path if needed)
OPENAPI_SPEC_PATH = os.environ.get(
    "OPENAPI_SPEC",
    os.path.join(REPO_ROOT, "specs", "001-ai-guided-inspection", "contracts", "openapi.yaml"),
)

# API base URL(s) for contract/integration tests.
# Set INSPECTION_FUNCTIONS_BASE_URL to override. If unset, integration tests default to the
# Firebase Functions emulator (run make run-functions first).
# Legacy: INSPECTION_API_BASE_URL = single base for all (e.g. when using Hosting).
EMULATOR_HOST = os.environ.get("INSPECTION_EMULATOR_HOST", "127.0.0.1")
EMULATOR_PORT = os.environ.get("INSPECTION_EMULATOR_PORT", "5001")
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "mana-api-38663")
FIREBASE_REGION = os.environ.get("FIREBASE_FUNCTIONS_REGION", "us-central1")
_DEFAULT_EMULATOR_BASE = f"http://{EMULATOR_HOST}:{EMULATOR_PORT}/{FIREBASE_PROJECT_ID}/{FIREBASE_REGION}"

FUNCTIONS_BASE = os.environ.get("INSPECTION_FUNCTIONS_BASE_URL", "").rstrip("/") or _DEFAULT_EMULATOR_BASE
LEGACY_API_BASE = os.environ.get("INSPECTION_API_BASE_URL", "").rstrip("/")


def get_sessions_url():
    """Base URL for inspection_sessions function (create, get, complete)."""
    if FUNCTIONS_BASE:
        return f"{FUNCTIONS_BASE}/inspection_sessions"
    return LEGACY_API_BASE


def get_next_url():
    """Base URL for inspection_next function."""
    if FUNCTIONS_BASE:
        return f"{FUNCTIONS_BASE}/inspection_next"
    return LEGACY_API_BASE


def get_evidence_url():
    """Base URL for inspection_evidence function."""
    if FUNCTIONS_BASE:
        return f"{FUNCTIONS_BASE}/inspection_evidence"
    return LEGACY_API_BASE


def get_record_url():
    """Base URL for inspection_record function."""
    if FUNCTIONS_BASE:
        return f"{FUNCTIONS_BASE}/inspection_record"
    return LEGACY_API_BASE


def emulator_reachable():
    """Return True if the Functions emulator is reachable (for integration tests)."""
    import urllib.error
    import urllib.request

    base = get_sessions_url()
    if not base:
        return False
    url = f"{base}/api/v1/tenants/health-check/inspection_sessions"
    try:
        req = urllib.request.Request(url, method="GET", headers={"X-User-Id": "test"})
        urllib.request.urlopen(req, timeout=5)
    except urllib.error.HTTPError:
        return True  # Server responded (4xx/5xx) = emulator is up
    except urllib.error.URLError as e:
        # Connection refused, timeout, etc. = emulator not reachable
        return False
    except OSError:
        return False  # e.g. timeout on some platforms
    return True

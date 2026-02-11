# Cloud Functions for Firebase – Inspection API (multiple endpoints)
# Deploy with `firebase deploy`
# Clients call each function URL directly with path as in OpenAPI (e.g. /api/v1/tenants/{id}/inspection_sessions).

import json
from firebase_admin import initialize_app
from firebase_functions import https_fn
from firebase_functions.options import set_global_options

set_global_options(max_instances=10)
initialize_app()


def _response(body, status: int) -> https_fn.Response:
    """Build JSON response from (body, status) tuple."""
    return https_fn.Response(
        json.dumps(body) if body is not None else "{}",
        status=status,
        headers={"Content-Type": "application/json"},
    )


@https_fn.on_request()
def inspection_sessions(req: https_fn.Request) -> https_fn.Response:
    """Session lifecycle: POST create, GET session, POST complete."""
    from api.routes.inspection_sessions import handle_sessions_request

    body, status = handle_sessions_request(req)
    if body is None and status == 404:
        return https_fn.Response("Not found", status=404)
    return _response(body, status)


@https_fn.on_request()
def inspection_next(req: https_fn.Request) -> https_fn.Response:
    """Submit answer and get next prompt (POST .../next)."""
    from api.routes.inspection_next import handle_next_request

    body, status = handle_next_request(req)
    return _response(body, status)


@https_fn.on_request()
def inspection_evidence(req: https_fn.Request) -> https_fn.Response:
    """Add evidence (POST .../evidence)."""
    from api.routes.inspection_evidence import handle_evidence_request

    body, status = handle_evidence_request(req)
    return _response(body, status)


@https_fn.on_request()
def inspection_record(req: https_fn.Request) -> https_fn.Response:
    """Get inspection record (GET .../record)."""
    from api.routes.inspection_record import handle_record_request

    body, status = handle_record_request(req)
    return _response(body, status)

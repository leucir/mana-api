# Quickstart: AI-First Guided Inspection

**Branch**: `001-ai-guided-inspection`

## Prerequisites

- Python 3.11+
- Firebase CLI (`firebase-tools`)
- Make (optional; commands can be run directly)

## Environment

- Copy or create env config for **dev** / **test** / **prod** (see plan: configuration via env and config files).
- Required env vars (examples): `GOOGLE_CLOUD_PROJECT`, `FIRESTORE_EMULATOR_HOST` (for local), `LLM_ENDPOINT` (or equivalent for Langgraph), tenant/config overrides as needed.

## Repository layout (this feature)

- **API**: `functions/api/` – routes and middleware for inspection endpoints.
- **Domain**: `functions/model/` – entities and aggregates (session, step, observation, evidence).
- **AI**: `functions/ai/` – Langgraph workflow, prompts, LLM client.
- **Infrastructure**: `functions/infrastructure/` – Firestore, Storage, config factories.
- **Tests**: `tests/` – unit, integration, contract (see OpenAPI in `specs/001-ai-guided-inspection/contracts/`).

## Run locally

1. **Firestore emulator** (recommended for dev):
   ```bash
   firebase emulators:start --only firestore
   ```
2. **Cloud Functions** (four functions: inspection_sessions, inspection_next, inspection_evidence, inspection_record):
   ```bash
   firebase emulators:start --only functions
   ```
   Or `cd functions && pip install -r requirements.txt` and run the Functions emulator. The client uses **four base URLs** (one per function) and sends the path as in the OpenAPI (e.g. `/api/v1/tenants/{tenantId}/inspection_sessions`).

## Test

- **Unit**: `pytest tests/unit` (or `make test-unit`).
- **Integration**: Point at Firestore emulator (and optional LLM endpoint); `pytest tests/integration`.
- **Contract**: Validate API against `specs/001-ai-guided-inspection/contracts/openapi.yaml` (e.g. with OpenAPI validators or contract tests that hit the API).

Tests use real LLM endpoint when configured (see tech_1); otherwise mocks for CI.

## Deploy

- **Firebase**: `firebase deploy --only functions,firestore,storage` (or per-environment).
- Ensure Firestore rules and Storage rules enforce tenant isolation (see data-model.md and constitution).

## Key flows (for manual testing)

Use the **function URL** for each operation as the request base; send the path as below.

1. **Create session**: POST to `{inspection_sessions_url}/api/v1/tenants/{tenantId}/inspection_sessions` with body `{ "intent": { "goal": "Inspect vehicle before purchase" } }` → expect 201 and initial steps or first prompt.
2. **Next prompt**: POST to `{inspection_next_url}/api/v1/tenants/{tenantId}/inspection_sessions/{sessionId}/next` with `{ "answer": "..." }` → expect next prompt or completion.
3. **Add evidence**: POST to `{inspection_evidence_url}/api/v1/tenants/{tenantId}/inspection_sessions/{sessionId}/evidence` with observationId and type/payload or storagePath.
4. **Get record**: GET `{inspection_record_url}/api/v1/tenants/{tenantId}/inspection_sessions/{sessionId}/record` (after completion) → decision-ready summary.

## Docs and contracts

- **Spec**: [spec.md](./spec.md)
- **Plan**: [plan.md](./plan.md)
- **Data model**: [data-model.md](./data-model.md)
- **API contract**: [contracts/openapi.yaml](./contracts/openapi.yaml)
- **Research**: [research.md](./research.md)

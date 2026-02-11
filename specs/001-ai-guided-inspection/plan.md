# Implementation Plan: AI-First Guided Inspection Module

**Branch**: `001-ai-guided-inspection` | **Date**: 2025-02-03 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/001-ai-guided-inspection/spec.md`

## Summary

Deliver an AI-first, guided inspection experience where users state intent in natural language; the system creates a session, drives an incremental question-by-question flow (with adaptation via Langgraph), and produces an attributable, decision-ready inspection record. Backend is Python Cloud Functions on Firebase with Firestore and Cloud Storage; state uses a lightweight Observer pattern; code is organized into api, model, ai, and tests with configuration and factory patterns for environment and external resources.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: Firebase (Cloud Functions, Firestore, Cloud Storage), Langgraph (AI workflow orchestration), LLM client with streaming support  
**Storage**: Firestore (inspection sessions, steps, observations, collaboration); Cloud Storage (evidence files)  
**Testing**: pytest; contract and integration tests; optional real LLM endpoint for E2E  
**Target Platform**: Firebase (serverless); clients consume APIs  
**Project Type**: backend API (single backend, no frontend in this scope)  
**Performance Goals**: Single-interaction session creation; one prompt at a time; streaming where applicable  
**Constraints**: Tenant isolation (multi-tenancy); attributable/reviewable records; env-based config (dev/test/prod)  
**Scale/Scope**: Multi-tenant; inspections per tenant; evidence and collaboration per inspection

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|--------|
| 1. Security non-negotiable | Pass | Auth and tenant isolation in design; no silent mutations (FR-012). |
| 2. Multi-tenancy first-class | Pass | Data model and APIs tenant-scoped; config per environment. |
| 3. TDD first | Pass | Tests before production code; research and plan reference test strategy. |
| 4. DDD defines system | Pass | Domain model in /model (entities, aggregates); ubiquitous language in spec/plan. |
| 5. OOP required | Pass | Encapsulation in domain objects; composition; /model holds behavior. |
| 6. UX competitive advantage | Pass | Loading, empty, error, offline in acceptance criteria and edge cases. |
| 7. AI encouraged | Pass | Langgraph + LLM for guided flow and adaptation. |
| 8. Clear boundaries | Pass | api / model / ai / tests separation; dependencies inward. |
| 9. Reliability & observability | Pass | User-friendly failures; logging/metrics/tracing with tenant isolation. |
| 10. Maintainability | Pass | Config/factory patterns; readable structure; docs. |
| 11. Documentation mandatory | Pass | research.md, data-model.md, contracts, quickstart. |
| 12. Technology stack fixed | Pass | Firebase (Cloud Functions Python, Firestore, Cloud Storage, Hosting). |

No violations. Complexity Tracking table left empty.

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-guided-inspection/
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1
├── contracts/           # Phase 1 (OpenAPI, etc.)
└── tasks.md             # Phase 2 (/speckit.tasks – not created by plan)
```

### Source Code (repository root)

```text
functions/                 # Firebase Cloud Functions (Python)
├── api/                   # HTTP/API layer (client + admin)
│   ├── routes/
│   └── middleware/
├── model/                 # Domain entities, aggregates, invariants
│   ├── entities/
│   └── aggregates/
├── ai/                    # Langgraph workflow, prompts, LLM integration
│   ├── graph/
│   ├── prompts/
│   └── clients/
├── infrastructure/        # Firestore, Storage, config, factories
│   ├── persistence/
│   └── config/
└── main.py                # Multiple HTTP Cloud Function entrypoints

tests/
├── unit/
├── integration/
└── contract/
```

**Structure Decision**: Backend-only API aligned with tech_1: `/api`, `/model`, `/ai`, plus `/infrastructure` for persistence and config. Tests at repo root under `tests/`. Firebase Functions live under `functions/` with subpackages for api, model, ai, infrastructure.

## API deployment

The inspection API is implemented as **multiple HTTP Cloud Functions** (one per route group). Clients call Cloud Functions directly; no Firebase Hosting rewrites are required for the API.

| Function name | Serves |
|---------------|--------|
| `inspection_sessions` | POST create session, GET session, POST complete |
| `inspection_next` | POST submit answer and get next prompt |
| `inspection_evidence` | POST add evidence |
| `inspection_record` | GET inspection record |

Each function has its own URL (e.g. `https://REGION-PROJECT.cloudfunctions.net/inspection_sessions`). The client sends the same path as in the OpenAPI contract (e.g. `/api/v1/tenants/{tenantId}/inspection_sessions`) as the request path to the appropriate function URL. Hosting can be added later to expose a single base URL if desired.

## Complexity Tracking

*(None – no constitution violations.)*

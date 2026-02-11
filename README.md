# mana-api

Backend API for **AI-first guided inspection**: users state intent in natural language; the system creates a session, drives a question-by-question flow (with optional adaptation via Langgraph), and produces an attributable, decision-ready inspection record.

**Stack:** Python 3.11+, Firebase (Cloud Functions, Firestore, Cloud Storage). Multi-tenant; tenant isolation and attributable records are required.

---

## Make commands

Run from repo root.

| Command | Description |
|--------|--------------|
| `make test` | Run unit, integration, and contract tests |
| `make test-unit` | Unit tests only (`tests/unit`) |
| `make test-integration` | Integration tests only (`tests/integration`) |
| `make test-contract` | Contract tests vs OpenAPI (`tests/contract`) |
| `make build` | Install Python deps in `functions/` |
| `make deploy` | Deploy functions, Firestore, Storage |
| `make lint` | Run ruff check in `functions/` |
| `make format` | Run ruff format in `functions/` |
| `make run-functions` | Install deps and run functions entrypoint (local) |

---

## High-level architecture

- **API:** Four HTTP Cloud Functions (clients call each function URL directly; path structure as in OpenAPI):
  - `inspection_sessions` — create session, get session, complete session
  - `inspection_next` — submit answer, get next prompt
  - `inspection_evidence` — add evidence
  - `inspection_record` — get inspection record

- **Layers (under `functions/`):**
  - **api/** — routes and middleware (auth, errors, response states)
  - **model/** — domain entities and aggregates (session, step, observation, evidence, record)
  - **ai/** — Langgraph workflow, prompts, LLM integration
  - **infrastructure/** — Firestore/Storage clients, config, persistence (repositories)

- **Tests (repo root):**
  - `tests/unit` — domain and unit tests
  - `tests/integration` — end-to-end flows
  - `tests/contract` — OpenAPI contract tests

- **Specs and contracts:** Feature spec, plan, data model, and OpenAPI live in `specs/001-ai-guided-inspection/`. See [quickstart](specs/001-ai-guided-inspection/quickstart.md) for env, run, and deploy.

---

## Docs and governance

- **Constitution:** [.specify/memory/constitution.md](.specify/memory/constitution.md) — principles and governance for the project.
- **Inspection feature:** [specs/001-ai-guided-inspection/](specs/001-ai-guided-inspection/) — spec, plan, data model, contracts, quickstart.

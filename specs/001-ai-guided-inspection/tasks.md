# Tasks: AI-First Guided Inspection Module

**Input**: Design documents from `specs/001-ai-guided-inspection/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included per constitution (TDD first). Write tests first; ensure they fail before implementation.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story (US1–US5)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `functions/` (api, model, ai, infrastructure); `tests/` at repository root
- Paths are relative to repo root: `/home/leucir/Documents/git/mana`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and structure per plan.md

- [ ] T001 Create directory structure in functions/ per plan: functions/api/routes, functions/api/middleware, functions/model/entities, functions/model/aggregates, functions/ai/graph, functions/ai/prompts, functions/ai/clients, functions/infrastructure/persistence, functions/infrastructure/config
- [ ] T002 Add Python 3.11+ and Firebase dependencies to functions/requirements.txt (firebase-admin, firebase-functions; Langgraph, LLM client; pytest for tests)
- [ ] T003 [P] Configure linting and formatting in functions/ (e.g. ruff, pyproject.toml or setup.cfg)
- [ ] T004 [P] Add environment configuration loader in functions/infrastructure/config/loader.py (dev/test/prod from env vars and config files per research.md)
- [ ] T005 Add Makefile at repo root with targets for test (unit, integration, contract), build, and deploy per tech_1

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure required before any user story. No user story work until this phase is complete.

- [ ] T006 Implement Firestore client factory in functions/infrastructure/persistence/firestore_client.py (tenant-scoped path pattern from data-model.md)
- [ ] T007 Implement Cloud Storage client factory in functions/infrastructure/persistence/storage_client.py for evidence file paths (tenant and session scoped)
- [ ] T008 [P] Implement tenant and auth middleware in functions/api/middleware/auth.py (extract tenantId and user id; enforce tenant isolation)
- [ ] T009 [P] Setup API routing base in functions/api/routes/ and wire to main.py HTTP entrypoints (Firebase Functions)
- [ ] T010 Add base error handling and user-friendly error responses in functions/api/middleware/errors.py
- [ ] T011 Add structured logging with tenant isolation in functions/infrastructure/config/logging.py (per constitution observability)
- [ ] T012 Implement config factory/builder for external resources (LLM endpoint, Firestore, Storage) in functions/infrastructure/config/factories.py so tests can inject mocks
- [ ] T059 [P] Define and implement loading, empty, error, and offline response contract for inspection API flows (constitution §6) in functions/api/middleware/response_states.py; document response shapes in specs/001-ai-guided-inspection/contracts/openapi.yaml
- [ ] T063 [P] Add metrics and distributed tracing with tenant isolation in functions/infrastructure/config/observability.py (constitution §9); ensure logging already in T011 is complemented by metrics and trace IDs

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: User Story 1 – Start inspection from intent and complete guided flow (Priority: P1) — MVP

**Goal**: User states intent in natural language; system creates session, presents one prompt at a time, allows evidence capture; produces structured inspection record.

**Independent Test**: Start inspection with stated intent, answer a sequence of single-question prompts, capture at least one evidence; verify complete inspection record exists with findings and evidence linked.

### Tests for User Story 1 (TDD – write first, ensure they fail)

- [ ] T013 [P] [US1] Contract test for POST create session in tests/contract/test_inspection_sessions_create.py (request/response against contracts/openapi.yaml)
- [ ] T014 [P] [US1] Contract test for POST submit answer and get next prompt in tests/contract/test_inspection_next.py
- [ ] T015 [P] [US1] Contract test for POST add evidence and GET record in tests/contract/test_inspection_evidence_and_record.py
- [ ] T016 [P] [US1] Integration test for full US1 journey (create session → answer prompts → add evidence → get record) in tests/integration/test_us1_guided_flow.py

### Implementation for User Story 1

- [ ] T017 [P] [US1] Create Intent and Target value objects in functions/model/entities/intent.py and functions/model/entities/target.py per data-model.md
- [ ] T018 [P] [US1] Create Step and Observation entities in functions/model/entities/step.py and functions/model/entities/observation.py with status and validation
- [ ] T019 [P] [US1] Create Evidence entity in functions/model/entities/evidence.py (type, storagePath, payload, createdBy)
- [ ] T020 [P] [US1] Create InspectionSession aggregate in functions/model/aggregates/inspection_session.py (intent, target, status, createdBy; invariants and state transitions from data-model.md)
- [ ] T021 [US1] Create InspectionRecord value object / output type in functions/model/entities/inspection_record.py (summary with findings, evidenceSummary, incomplete, followUps)
- [ ] T022 [US1] Implement session repository (save/load by tenantId and sessionId) in functions/infrastructure/persistence/session_repository.py using Firestore client
- [ ] T023 [US1] Implement step and observation persistence (subcollections under session) in functions/infrastructure/persistence/step_repository.py and observation_repository.py
- [ ] T024 [US1] Implement evidence persistence and Storage upload path in functions/infrastructure/persistence/evidence_repository.py
- [ ] T025 [US1] Implement Langgraph workflow for intent → initial steps and first prompt in functions/ai/graph/inspection_graph.py (no adaptation yet)
- [ ] T026 [US1] Implement prompt generation (one question at a time) in functions/ai/prompts/ and wire to graph
- [ ] T027 [US1] Implement create session handler: parse intent, create session, run graph for initial steps/first prompt, persist in functions/api/routes/inspection_sessions.py
- [ ] T060 [US1] Enforce environment config (FR-007) in API or domain: validate evidence types, evidence size/count limits per tenant, step libraries, role actions, and completion criteria against config from T004/T012; reject or constrain invalid requests in functions/api/routes/ or functions/model/ (e.g. evidence type and size validator)
- [ ] T061 [US1] When intent is vague or very short, return clarifying question or propose initial steps (no hard fail); implement branch in create-session flow and graph in functions/api/routes/inspection_sessions.py and functions/ai/graph/inspection_graph.py
- [ ] T028 [US1] Implement get session handler (for resumption) in functions/api/routes/inspection_sessions.py
- [ ] T029 [US1] Implement submit answer and get next prompt handler: persist observation, advance graph, return next prompt in functions/api/routes/inspection_next.py
- [ ] T030 [US1] Implement add evidence handler in functions/api/routes/inspection_evidence.py
- [ ] T031 [US1] Implement record generation from session (findings, evidence, incomplete, followUps) and GET record handler in functions/api/routes/inspection_record.py
- [ ] T065 [US1] Implement complete-session action: only primary user (session owner) can mark inspection complete; expose endpoint or action and reject non-owner with 403 in functions/api/routes/inspection_sessions.py
- [ ] T066 [P] [US1] Add session creation latency assertion (≤5s per SC-001a) in tests/integration/test_us1_guided_flow.py or tests/contract/test_inspection_sessions_create.py
- [ ] T032 [US1] Wire inspection routes to main.py HTTP functions with tenant path params

**Checkpoint**: User Story 1 independently testable (create → prompts → evidence → record)

---

## Phase 4: User Story 2 – System adapts the flow based on user answers (Priority: P2)

**Goal**: System reorders steps, adds steps, or branches into micro-flows when user input justifies it.

**Independent Test**: Run inspection, provide answer that implies new focus (e.g. damage); verify system adjusts subsequent steps or adds micro-flow.

### Tests for User Story 2

- [ ] T033 [P] [US2] Integration test for flow adaptation (answer implying new priority → verify step reorder/add/branch) in tests/integration/test_us2_adaptation.py

### Implementation for User Story 2

- [ ] T034 [US2] Extend Langgraph workflow in functions/ai/graph/inspection_graph.py with conditional edges for reorder, add, branch based on answer
- [ ] T035 [US2] Implement step reorder and add-step logic in functions/model/aggregates/inspection_session.py or domain service used by graph
- [ ] T036 [US2] Ensure submit-answer handler and graph use updated step list and return next prompt from adapted flow in functions/api/routes/inspection_next.py and functions/ai/graph/inspection_graph.py

**Checkpoint**: User Stories 1 and 2 both work; flow adapts when justified

---

## Phase 5: User Story 3 – Share inspection and collaborate mid-stream (Priority: P3)

**Goal**: User shares inspection; participants add comments, follow-up tasks, evidence; contributions integrated into plan and attributable.

**Independent Test**: Share in-progress inspection, collaborator adds comment and one evidence; both appear in record and are attributable.

### Tests for User Story 3

- [ ] T037 [P] [US3] Contract test for share and collaboration endpoints in tests/contract/test_inspection_collaboration.py
- [ ] T038 [P] [US3] Integration test for share and collaborator contribution in tests/integration/test_us3_collaboration.py

### Implementation for User Story 3

- [ ] T039 [P] [US3] Create Collaboration entity in functions/model/entities/collaboration.py (type: comment, follow_up_task, evidence; content, createdBy, linkedStepId)
- [ ] T040 [US3] Implement collaboration repository (subcollection under session) in functions/infrastructure/persistence/collaboration_repository.py
- [ ] T041 [US3] Implement share session handler: issue shareable link for session; participants with link can join (link scoped/revocable per implementation) in functions/api/routes/inspection_share.py
- [ ] T067 [US3] Enforce collaborator permissions: reject add/reorder steps from non-primary users; accept only comment, follow_up_task, evidence in functions/api/routes/inspection_collaboration.py
- [ ] T042 [US3] Implement add collaboration handler and incorporate contributions into plan in functions/api/routes/inspection_collaboration.py
- [ ] T062 [US3] When a collaborator contribution conflicts with current plan, detect and surface conflict (e.g. flag in response or plan) so record stays consistent and attributable; implement in functions/api/routes/inspection_collaboration.py or domain used by it
- [ ] T064 [US3] Ensure record remains consistent and attributable under concurrent collaborator edits (e.g. ordering, version field, or merge rules) in functions/infrastructure/persistence/collaboration_repository.py and session/record writes
- [ ] T043 [US3] Include collaboration in record generation (attributable comments, follow-ups) in functions/api/routes/inspection_record.py and record model
- [ ] T044 [US3] Wire share and collaboration routes in main.py

**Checkpoint**: User Stories 1–3 work; collaboration attributable in record

---

## Phase 6: User Story 4 – Decision-ready, trustworthy inspection record (Priority: P4)

**Goal**: Record is attributable, reviewable, reversible; summary includes findings, evidence, incomplete, follow-ups; no silent AI mutations.

**Independent Test**: Complete inspection (with optional collaboration); verify summary has findings, evidence, incomplete, follow-ups; each finding traceable to evidence and actor.

### Tests for User Story 4

- [ ] T045 [P] [US4] Integration test for record completeness and attribution in tests/integration/test_us4_record_trust.py

### Implementation for User Story 4

- [ ] T046 [US4] Enforce attribution on every finding and evidence in record generation (createdBy, timestamps) in functions/model/entities/inspection_record.py and functions/api/routes/inspection_record.py
- [ ] T047 [US4] Add record version field and ensure all changes are reviewable (no silent overwrites) in functions/infrastructure/persistence/ and record generation
- [ ] T048 [US4] Document record schema and attribution guarantees in specs/001-ai-guided-inspection/data-model.md (InspectionRecord section)

**Checkpoint**: Record is decision-ready and trustworthy

---

## Phase 7: User Story 5 – Coverage- and relevance-aware guidance (Priority: P5)

**Goal**: Track what is checked vs intent; nudge back to critical items when user skips; record low-priority notes but steer back to goal.

**Independent Test**: Start with clear intent, skip high-value check → system surfaces nudge; add low-priority observation → system steers back to goal.

### Tests for User Story 5

- [ ] T049 [P] [US5] Integration test for coverage nudge and relevance steer in tests/integration/test_us5_coverage_relevance.py

### Implementation for User Story 5

- [ ] T050 [US5] Implement coverage tracking (checked vs implied by intent) in functions/ai/graph/ or domain service used by graph
- [ ] T051 [US5] Add nudge logic when critical checks are skipped (inject prompt or step) in functions/ai/graph/inspection_graph.py
- [ ] T052 [US5] Add relevance logic: record low-priority observations but next prompt steers to goal in functions/ai/prompts/ and graph
- [ ] T053 [US5] Ensure incomplete critical items appear in record summary in functions/api/routes/inspection_record.py

**Checkpoint**: All five user stories independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, hardening, and validation across stories

- [ ] T054 [P] Update quickstart.md with any new env vars or commands in specs/001-ai-guided-inspection/quickstart.md
- [ ] T055 [P] Add unit tests for domain entities and aggregates in tests/unit/model/ (invariants, state transitions)
- [ ] T056 Add Firestore and Storage security rules for tenant isolation (firestore.rules, storage.rules at repo root)
- [ ] T057 Run full test suite and quickstart validation (make test; manual quickstart steps)
- [ ] T058 Add regression test for edge cases from spec (vague intent, offline resumption, concurrent collaborators) in tests/integration/test_edge_cases.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — blocks all user stories
- **Phase 3 (US1)**: Depends on Phase 2 — MVP
- **Phase 4 (US2)**: Depends on Phase 3 (extends graph and flow)
- **Phase 5 (US3)**: Depends on Phase 3 (adds share and collaboration on top of session)
- **Phase 6 (US4)**: Depends on Phase 3 (record refinement; can overlap with US3)
- **Phase 7 (US5)**: Depends on Phase 3 and 4 (coverage/relevance in graph)
- **Phase 8 (Polish)**: Depends on completion of desired user stories

### User Story Dependencies

- **US1 (P1)**: After Foundational only — no other story required
- **US2 (P2)**: Builds on US1 (same graph, add adaptation)
- **US3 (P3)**: Builds on US1 (same session, add share/collaboration)
- **US4 (P4)**: Builds on US1 (record already in US1; US4 tightens attribution and schema)
- **US5 (P5)**: Builds on US1 and US2 (coverage/relevance in graph)

### Within Each User Story

- Contract and integration tests (TDD) before implementation
- Entities/aggregates before repositories and handlers
- Repositories and graph before API routes
- Wire routes in main.py last for that story

### Parallel Opportunities

- Phase 1: T003, T004 [P]
- Phase 2: T008, T009 [P]; T059, T063 [P] (UX response states, observability)
- Phase 3: T013–T016 [P] (all US1 tests); T017–T020 [P] (entities); T021 can follow
- Phase 4: T033 [P]
- Phase 5: T037, T038 [P]; T039 [P]
- Phase 6: T045 [P]
- Phase 7: T049 [P]
- Phase 8: T054, T055 [P]
- Different stories: US2, US3, US4, US5 can be worked in parallel after US1 (with coordination on shared graph and record)

---

## Parallel Example: User Story 1

```bash
# Tests first (all in parallel):
T013 Contract test create session    → tests/contract/test_inspection_sessions_create.py
T014 Contract test next prompt        → tests/contract/test_inspection_next.py
T015 Contract test evidence and record → tests/contract/test_inspection_evidence_and_record.py
T016 Integration test US1 journey     → tests/integration/test_us1_guided_flow.py

# Then entities (parallel):
T017 Intent, Target                   → functions/model/entities/intent.py, target.py
T018 Step, Observation                → functions/model/entities/step.py, observation.py
T019 Evidence                         → functions/model/entities/evidence.py
T020 InspectionSession aggregate      → functions/model/aggregates/inspection_session.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup  
2. Complete Phase 2: Foundational  
3. Complete Phase 3: User Story 1 (tests first, then implementation)  
4. **STOP and VALIDATE**: Run contract and integration tests for US1  
5. Deploy/demo MVP (create session → prompts → evidence → record)

### Incremental Delivery

1. Setup + Foundational → foundation ready  
2. US1 → test independently → deploy (MVP)  
3. US2 → adaptation → test → deploy  
4. US3 → share and collaboration → test → deploy  
5. US4 → record trust and attribution → test → deploy  
6. US5 → coverage and relevance → test → deploy  
7. Polish → docs, rules, edge-case tests  

### Parallel Team Strategy

- After Foundational: one developer on US1 (critical path for MVP)  
- After US1: Developer A — US2; Developer B — US3; Developer C — US4/US5  
- Merge and integrate; run full test suite before Polish  

---

## Notes

- [P] = different files, no dependencies; safe to run in parallel  
- [USn] = task belongs to that user story for traceability  
- Each user story is independently testable per spec  
- TDD: write tests (T013–T016, etc.), ensure they fail, then implement  
- Commit after each task or logical group  
- Paths are under `functions/` and `tests/` at repo root  
- **Remediation (post-analyze)**: T059 (UX states, constitution §6), T060 (FR-007 enforce config), T061 (vague intent → clarify), T062 (surface collaborator conflict), T063 (metrics/tracing, constitution §9), T064 (concurrent collaborators) address specification analysis findings C1, G1, U1, U2, C2, U3.
- **Clarifications (spec)**: T065 (primary user only can complete), T066 (5s latency validation), T041 updated (shareable link), T067 (collaborators no add/reorder steps), T060 updated (evidence size/count per tenant).  

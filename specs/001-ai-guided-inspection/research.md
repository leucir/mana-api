# Research: AI-First Guided Inspection Module

**Branch**: `001-ai-guided-inspection`  
**Date**: 2025-02-03

## 1. Langgraph for inspection workflow orchestration

**Decision**: Use Langgraph to orchestrate the inspection workflow (intent → initial steps, question loop, adaptation, coverage/relevance).

**Rationale**: Langgraph provides stateful, graph-based orchestration over LLM calls; supports conditional edges (reorder, add, branch) and human-in-the-loop style steps. Fits the “incremental prompt → answer → adapt” loop and keeps workflow logic explicit and testable.

**Alternatives considered**: Raw LangChain chains (less structure for branching); custom state machine (more code, no built-in LLM integration); single-prompt “mega” flows (harder to keep attributable and step-wise).

---

## 2. Firestore data model for inspections

**Decision**: Model inspections as a small set of top-level collections with subcollections where needed; use document IDs that support tenant isolation and efficient queries (e.g. `tenants/{tenantId}/inspection_sessions/{sessionId}`); store steps and observations as subcollections or embedded arrays depending on size and query patterns (see data-model.md).

**Rationale**: Firestore favors shallow, wide structures and client-friendly queries; tenant prefix in path enforces multi-tenancy at the data layer; subcollections allow unbounded steps/observations without single-document size limits.

**Alternatives considered**: Single “inspection” document with nested steps/observations (risk of 1 MiB limit); separate top-level collections with tenantId field (works but path-based isolation is clearer for rules and auditing).

---

## 3. Observer / Pub-Sub for inspection state in serverless

**Decision**: Use a lightweight in-process Observer pattern within the Cloud Function to notify “listeners” when inspection state (current step, observations, evidence) changes, so that the Langgraph workflow and any side-effects (e.g. persistence, metrics) stay in sync without introducing a separate message broker for this feature.

**Rationale**: Cloud Functions are stateless; state lives in Firestore. “State” here means the in-memory state during a request (e.g. the graph state). An observer that reacts to state transitions (e.g. step completed, evidence added) keeps the workflow and persistence layer decoupled and testable. For cross-request or cross-user events (e.g. collaborator joined), Firestore listeners or callable triggers can be used later; not required for MVP.

**Alternatives considered**: Firebase Pub/Sub (overkill for single-request workflow; adds latency and ops). Firestore onSnapshot in a long-lived client (out of scope for backend-only). Pure functional “state in, state out” with no observers (acceptable; observer is optional refinement for clarity and future extensibility).

---

## 4. Streaming for LLM responses

**Decision**: Use streaming when calling LLMs for prompt generation or reasoning so that the client can show progress and reduce perceived latency where the API exposes a streaming endpoint.

**Rationale**: Aligns with tech_1; improves UX (first token faster); backend can still consume stream and persist a single attributable answer.

**Alternatives considered**: Non-streaming only (simpler; acceptable if streaming not available). SSE/WebSocket from Function to client (implementation detail; contracts can define later).

---

## 5. Configuration and external resources

**Decision**: External resources (LLM endpoint, Firestore, Storage, feature flags) are configured via environment variables and configuration files per environment (dev/test/prod). Use factory/builder patterns to construct clients and repositories so that tests can inject mocks or test doubles.

**Rationale**: Matches tech_1; supports tenant- and environment-specific behavior (FR-007) and keeps the codebase testable and deployable across environments.

**Alternatives considered**: Hardcoded endpoints (rejected). Runtime-only config (rejected for build-time choices like which step libraries are enabled).

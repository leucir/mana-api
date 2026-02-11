<!--
Sync Impact Report
==================
Version change: (none) → 1.0.0
Modified principles: N/A (initial creation)
Added sections: All principle sections, Governance, Conflict Priority
Removed sections: None
Templates: .specify/templates/plan-template.md — ⚠ not present
           .specify/templates/spec-template.md — ⚠ not present
           .specify/templates/tasks-template.md — ⚠ not present
           .specify/templates/commands/*.md — ⚠ not present
Follow-up TODOs: Create templates when adopting full speckit workflow; align plan/spec/tasks to constitution.
-->

# Project Constitution: mana-api

**Version:** 1.1.0  
**Ratification date:** 2025-02-03  
**Last amended:** 2025-02-05

## Purpose

This constitution defines the non-negotiable principles and governance for the mana-api project. All specifications, implementation plans, and code MUST align with these principles. When principles conflict, the Conflict Priority order in Governance applies.

## Principles

### 1. Security is non-negotiable

Security and privacy are mandatory. Design and implementation MUST treat security as a first-class constraint, not an afterthought. No feature or delivery pressure overrides security requirements.

**Rationale:** Breaches cause lasting harm; security cannot be retrofitted reliably.

### 2. Multi-tenancy is a first-class concern

Multi-tenancy MUST be considered from design through deployment. Data, configuration, and runtime behavior MUST respect tenant isolation. All features and infrastructure MUST be tenant-aware where applicable.

**Rationale:** Tenant isolation is required for correctness, compliance, and trust.

### 3. Test-Driven Development comes first

- No production code without a failing test.
- Tests define behavior; code exists to satisfy tests.
- Bugs require regression tests.
- **Test pyramid is enforced:**
  - **Unit tests (static):** Must exist for domain logic, entities, and critical paths; no external services; run with `make test-unit` and must pass before merge.
  - **Integration tests (emulators):** Must exist for API and end-to-end flows; run against Firebase emulators (Functions, and Firestore where applicable); start emulators with `make run-functions` (or equivalent), then run `make test-integration`; tests may skip with a clear message if the emulator is not reachable.
  - **Contract tests:** Must exist where an API contract (e.g. OpenAPI) is defined; validate request/response against the contract; run with `make test-contract`.
  - All three layers (unit, integration, contract) must be implemented and maintained; CI or pre-merge checks should run unit and, when possible, integration and contract tests.

**Rationale:** TDD ensures correctness, safe refactoring, and living documentation of behavior.

### 4. Domain-Driven Design defines the system

- The domain model is the source of truth.
- Entities, aggregates, and invariants live in the domain layer.
- Ubiquitous language is used consistently in specs, tests, and code.

**Rationale:** DDD keeps the system aligned with business reality and prevents anemic or scattered logic.

### 5. Object-Oriented design is required

- Encapsulate behavior and invariants inside objects.
- Prefer composition over inheritance.
- Avoid anemic models and god objects.

**Rationale:** OOP supports maintainability, testability, and clear boundaries.

### 6. User experience is a competitive advantage

- Performance, clarity, and accessibility are product features.
- Every flow defines loading, empty, error, and offline states.
- UX requirements are part of acceptance criteria.

**Rationale:** UX directly affects adoption and satisfaction; it is a product requirement, not optional.

### 7. AI is encouraged

Use AI whenever possible in the capabilities. AI-assisted design, implementation, and documentation are encouraged within the bounds of this constitution.

**Rationale:** Leveraging AI improves delivery and quality when governed by principles.

### 8. Architecture enforces clear boundaries

- UI, application, domain, and infrastructure are cleanly separated.
- Dependencies point inward (e.g., infrastructure depends on domain, not the reverse).

**Rationale:** Clear boundaries enable independent evolution and testing of layers.

### 9. Reliability and observability are mandatory

- Failures are user-friendly and diagnosable.
- Logging, metrics, and tracing respect security and tenant isolation.

**Rationale:** Operability and debuggability are required for production readiness.

### 10. Maintainability beats short-term speed

- Code MUST be readable, testable, and evolvable.
- Delivery speed is optimized only after correctness, security, and UX.

**Rationale:** Short-term shortcuts create long-term debt; maintainability protects the codebase.

### 11. Documentation is mandatory

- Every feature and domain concept MUST be documented.
- Documentation includes explanations, sample code, and diagrams where relevant.
- Undocumented behavior is considered incomplete.
- **README maintenance:** After each implementation (or significant change), the project README MUST be refreshed with additional and useful information: high-level project description, make commands, high-level architecture (layers, APIs, tests), and pointers to specs and constitution. The README is the main entry point for the repository and must stay current.

**Rationale:** Documentation enables onboarding, audits, and safe evolution.

### 12. Technology stack is fixed

- **Backend:** Firebase
  - Cloud Functions (Python)
  - Firestore
  - Cloud Storage
  - Firebase Hosting (for backend test)

Choices outside this stack require an explicit amendment or documented exception.

**Rationale:** A fixed stack reduces variability and supports consistent operations and skills.

## Governance

### Amendment procedure

- Propose changes to this document (or new principles) in a structured amendment.
- Update version and Last amended date when changes are adopted.
- Propagate changes to plan, spec, and task templates and any runtime guidance (e.g., README, quickstart).

### Versioning policy

- **MAJOR:** Backward-incompatible governance or principle removals/redefinitions.
- **MINOR:** New principle or section, or materially expanded guidance.
- **PATCH:** Clarifications, wording, typo fixes, non-semantic refinements.

### Conflict priority

When principles conflict, they are applied in this order:

1. Correctness and safety (TDD, invariants, tests)
2. Security and privacy
3. User experience
4. Domain integrity (DDD and domain boundaries)
5. Delivery speed and convenience
6. Multi-tenancy isolation
7. Maintainability and architectural clarity

### Compliance

- Specifications and plans MUST reference this constitution and align with the principles.
- Reviews MUST check alignment with the conflict priority when trade-offs are made.
- Incomplete or undocumented behavior is considered non-compliant.

# Feature Specification: AI-First Guided Inspection Module

**Feature Branch**: `001-ai-guided-inspection`  
**Created**: 2025-02-03  
**Status**: Draft  
**Input**: User description: "Mana's Inspection module as an AI-first, guided inspection experience where the primary input is user intent in natural language; adaptive step-by-step execution; generic inspection engine; coverage- and relevance-aware guidance; built-in collaboration; attributable, decision-ready inspection records."

## Clarifications

### Session 2025-02-03

- Q: Which sharing model (invite, link, role-based) should the product use for inspections? → A: Link-based (shareable link).
- Q: Who can mark an inspection complete? → A: Primary user only.
- Q: Target latency for session creation / first prompt? → A: Under 5 seconds.
- Q: Can collaborators add or reorder steps? → A: No; comments, follow-ups, and evidence only.
- Q: Evidence file size or count limits? → A: Configurable per tenant.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start inspection from intent and complete guided flow (Priority: P1)

A user states what they want to accomplish in natural language (e.g., inspecting a vehicle before purchase, walking a property before move-in) and any constraints (time, environment, priorities). The system creates an inspection session and guides them through an incremental, question-by-question flow. Each prompt is a single, actionable ask. The user captures evidence as they go. At the end, the system produces a structured, auditable inspection record.

**Why this priority**: This is the core value: intent in, structured record out, without rigid templates or long forms.

**Independent Test**: Can be fully tested by starting a new inspection with a stated intent, answering a sequence of single-question prompts, and capturing at least one piece of evidence; the test passes when a complete inspection record exists with findings and evidence linked.

**Acceptance Scenarios**:

1. **Given** no active inspection, **When** the user states their inspection goal and constraints in natural language, **Then** the system creates an inspection session and presents an initial set of steps or a first prompt.
2. **Given** an active inspection session, **When** the user is shown a prompt, **Then** the prompt asks for one thing at a time and is actionable in the moment.
3. **Given** the user has answered prompts and captured evidence, **When** the inspection is completed, **Then** the system produces a structured record that includes what was found and what evidence supports it.
4. **Given** the user has stated intent and constraints, **When** the session is initialized, **Then** the experience feels like an interactive guide, not a static checklist.

---

### User Story 2 - System adapts the flow based on user answers (Priority: P2)

As the user answers, the system can reorder steps, add new steps, or branch into short micro-flows when the user reports something unexpected. The flow remains suitable for both planned workflows and ad-hoc discovery.

**Why this priority**: Adaptation is what makes the experience AI-first and flexible; without it, the product is a fixed wizard.

**Independent Test**: Can be tested by running an inspection, providing an answer that implies a new or different focus (e.g., reporting damage), and verifying that the system adjusts the subsequent steps or adds a micro-flow.

**Acceptance Scenarios**:

1. **Given** an inspection in progress, **When** the user’s answer indicates something unexpected or a new priority, **Then** the system may reorder, add, or branch steps and present the next prompt accordingly.
2. **Given** a planned sequence of steps, **When** the user skips or diverges, **Then** the system can still guide them toward completion without forcing a rigid order.
3. **Given** any inspection type, **When** the user discovers information mid-flow, **Then** the system incorporates that into the evolving plan so that important checks are not dropped.

---

### User Story 3 - Share inspection and collaborate mid-stream (Priority: P3)

The user shares an inspection while it is in progress. Other participants can contribute comments, follow-up tasks, and additional evidence. Their contributions are incorporated into the inspection’s evolving plan so that suggestions become actionable at the right time. The flow remains a shared working session but stays structured and traceable.

**Why this priority**: Collaboration is required by the product vision but builds on the core guided flow.

**Independent Test**: Can be tested by sharing an in-progress inspection with a collaborator, having them add a comment and one piece of evidence, and verifying both appear in the inspection record and are attributable to the collaborator.

**Acceptance Scenarios**:

1. **Given** an in-progress inspection, **When** the user shares it with another participant, **Then** that participant can view the inspection and add comments, follow-up tasks, or evidence.
2. **Given** a collaborator has added a comment or follow-up, **When** the inspection plan is updated, **Then** that contribution is reflected in the plan and can be addressed in the flow.
3. **Given** multiple contributors, **When** the inspection record is produced, **Then** each contribution is attributable and traceable without breaking the guided flow.

---

### User Story 4 - Decision-ready, trustworthy inspection record (Priority: P4)

The system produces a final inspection record that is usable and trustworthy: what was found, what evidence supports it, what remains incomplete (if anything), and what follow-ups were created. Guidance does not silently mutate reality; the output is attributable, reviewable, and reversible.

**Why this priority**: Trust and auditability are mandatory for adoption; the record is the deliverable.

**Independent Test**: Can be tested by completing an inspection (including optional collaboration) and verifying that the summary includes findings, evidence, incomplete items, and follow-ups, and that each finding can be traced to evidence and actor.

**Acceptance Scenarios**:

1. **Given** a completed inspection, **When** the user requests or receives the final record, **Then** it includes a clear summary of what was found, what evidence supports it, what is incomplete, and what follow-ups exist.
2. **Given** any change or suggestion from the system, **When** it affects what is recorded, **Then** the change is attributable and reviewable (no silent “magic” mutations).
3. **Given** the record, **When** a stakeholder reviews it, **Then** they can use it to make decisions without needing to re-run the inspection.

---

### User Story 5 - Coverage- and relevance-aware guidance (Priority: P5)

The system tracks what has been checked against what is implied by the user’s intent and nudges the user back to critical items if they skip ahead or get distracted. It avoids derailing the flow by over-focusing on irrelevant observations: low-priority notes can be recorded, but the user is gently steered back to the goal. The principle is to keep the user moving forward while still producing thorough, decision-ready results.

**Why this priority**: Improves quality and completeness without blocking the flow; depends on core flow and intent.

**Independent Test**: Can be tested by starting an inspection with a clear intent, skipping a high-value check, and verifying that the system surfaces a nudge or prompt to address it; and by adding a low-priority observation and verifying the system does not derail the main flow.

**Acceptance Scenarios**:

1. **Given** user intent that implies certain critical checks, **When** the user skips or diverts from them, **Then** the system nudges them back to those items without forcing a rigid sequence.
2. **Given** the user adds a low-priority or tangential observation, **When** it is recorded, **Then** the system steers the user back to the primary goal rather than expanding on the tangent.
3. **Given** the session, **When** the system suggests next steps, **Then** it balances coverage (not missing important items) with relevance (not over-focusing on irrelevant ones).

---

### Edge Cases

- What happens when the user’s intent is vague or very short? The system MUST still create a session and propose an initial set of steps or ask a clarifying question rather than failing. When the system asks a clarifying question, it returns that as the first prompt (no initial steps yet) so the user can refine intent; the session remains created and resumable.
- What happens when the user goes offline mid-inspection? The system MUST allow resumption and preserve partial progress; the record MUST reflect what was completed and what was not.
- What happens when a collaborator adds a follow-up that conflicts with the current plan? The system MUST incorporate or surface the conflict in a way that keeps the record consistent and attributable.
- What happens when the user never completes critical checks implied by intent? The record MUST clearly indicate what remains incomplete so that stakeholders can act on it.
- How does the system handle multiple concurrent collaborators editing or adding evidence? Contributions MUST be attributable and the record MUST remain consistent and reviewable.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept the user’s inspection goal and constraints in natural language and create an inspection session from that intent.
- **FR-002**: System MUST present prompts one at a time, each actionable in the moment and tuned to reduce cognitive load.
- **FR-003**: System MUST propose an initial set of steps (or equivalent) from the user’s intent and drive execution through an incremental, question-by-question loop.
- **FR-004**: System MUST allow the user to capture evidence (e.g., notes, media, structured data) and associate it with steps or observations.
- **FR-005**: System MUST adapt the flow by reordering steps, adding steps, or branching into short micro-flows when user input justifies it.
- **FR-006**: System MUST operate on generic concepts (e.g., targets, steps, observations, evidence, collaboration) and MUST NOT be hardcoded for a single inspection type.
- **FR-007**: System MUST support configuration (via API or product) to enforce what is allowed in a given environment: evidence types, step libraries or reasoning policies, role actions, completion criteria, and evidence size/count limits (e.g. max file size, max evidence items per observation or per session) per tenant.
- **FR-008**: System MUST track what has been checked against what is implied by the user’s intent and MUST nudge the user back to critical items when they skip or get distracted.
- **FR-009**: System MUST avoid derailing the flow by over-focusing on irrelevant observations; it MAY record low-priority notes but MUST steer the user back to the goal.
- **FR-010**: System MUST allow an inspection to be shared mid-stream via a shareable link; participants with the link can contribute comments, follow-up tasks, and evidence. Collaborators MUST NOT add or reorder steps; only the primary user and the system (via adaptation) control the step sequence.
- **FR-011**: System MUST incorporate collaborators’ contributions into the inspection’s evolving plan so that suggestions become actionable at the right time.
- **FR-012**: System MUST produce an inspection record that is attributable, reviewable, and reversible; AI-driven guidance MUST NOT silently mutate recorded reality.
- **FR-013**: System MUST produce a decision-ready summary including what was found, what evidence supports it, what remains incomplete, and what follow-ups were created.
- **FR-014**: System MUST support resumption after interruption (e.g., offline) and preserve partial progress; the record MUST reflect completed vs incomplete state.

### Key Entities

- **Inspection session**: A single run of an inspection, tied to a user’s intent and constraints; has a lifecycle (created, in progress, completed) and contains steps, observations, and evidence. Transition to completed is initiated only by the primary user (session owner).
- **Intent**: The user’s stated goal and constraints (e.g., “inspect vehicle before purchase,” time available, environment); used to initialize the session and to drive coverage and relevance.
- **Target**: The inspectable subject (e.g., vehicle, property, equipment); generic so the engine supports any type.
- **Step**: A unit of work in the inspection (e.g., check brakes, document room condition); can be reordered, added, or branched.
- **Observation**: A recorded finding or note tied to a step or target; can be critical or low-priority for relevance guidance.
- **Evidence**: Captured material that supports an observation (notes, photos, measurements, etc.); must be attributable and linked to the record.
- **Collaboration**: Comments, follow-up tasks, and additional evidence from participants other than the primary user; must be integrated into the plan and the record. Collaborators do not add or reorder steps.
- **Inspection record**: The final output: summary of findings, supporting evidence, incomplete items, and follow-ups; must be decision-ready and trustworthy.

## Assumptions

- Users have a way to authenticate and are identified so that contributions and records can be attributable.
- “Natural language” input is in a supported language and of reasonable length; the system may ask for clarification when intent is ambiguous.
- Evidence types (e.g., photo, text, measurement) and evidence size/count limits (e.g. max file size, max items per observation) are configurable per tenant via environment configuration.
- Sharing is link-based: the primary user (owner) receives a shareable link; anyone with the link can join the inspection as a participant. The link may be scoped or revocable per implementation.
- Only the primary user (session owner) can mark the inspection complete; collaborators cannot change completion status.
- Offline support may be best-effort (e.g., queue and sync) with clear indication of incomplete or unsynced state in the record.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can start an inspection by describing their goal in natural language and receive an initial set of steps or a first prompt within a single interaction.
- **SC-001a**: Session creation returns initial steps or first prompt within 5 seconds (typical case; p95 target for validation).
- **SC-002**: Users complete the primary inspection flow with one prompt at a time; no step requires filling a long form to proceed.
- **SC-003**: In at least 80% of sessions where user input justifies a change, the system adapts the flow (reorders, adds, or branches) within the same session.
- **SC-004**: Collaborators can join a shared inspection and add at least one comment or evidence item that appears in the final record and is attributable to them.
- **SC-005**: The inspection record includes what was found, supporting evidence, incomplete items (if any), and follow-ups in a single decision-ready summary for 100% of completed inspections.
- **SC-006**: Users can resume an interrupted inspection and see their previous progress; the record correctly reflects what was completed before interruption and what remains.
- **SC-007**: Critical checks implied by the user’s intent are either completed or explicitly marked incomplete in the record, so stakeholders can act on gaps.

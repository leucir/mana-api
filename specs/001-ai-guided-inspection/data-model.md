# Data Model: AI-First Guided Inspection

**Branch**: `001-ai-guided-inspection`  
**Date**: 2025-02-03

Optimized for Firestore: tenant-scoped paths, subcollections for unbounded lists, and document sizes kept within limits.

---

## Entity overview

| Entity | Firestore role | Key relationships |
|--------|----------------|--------------------|
| InspectionSession | Root aggregate | Has Intent, Steps, Observations, Evidence refs, Collaboration |
| Intent | Embedded in session | — |
| Target | Embedded or subcollection | Referenced by Steps/Observations |
| Step | Subcollection under session | Ordered; may reference Target |
| Observation | Subcollection under session | Links to Step; has priority (critical/low) |
| Evidence | Subcollection or Storage refs | Linked to Observation; attributable |
| Collaboration | Subcollection (comments, follow-ups) | Attributable to participant |
| InspectionRecord | Derived / materialized view | Output of session completion |

---

## Firestore layout (conceptual)

```text
tenants/{tenantId}/
  inspection_sessions/{sessionId}
    # Document: InspectionSession aggregate (intent, status, metadata)
  inspection_sessions/{sessionId}/steps/{stepId}
  inspection_sessions/{sessionId}/observations/{observationId}
  inspection_sessions/{sessionId}/evidence/{evidenceId}
  inspection_sessions/{sessionId}/collaboration/{collaborationId}
```

Evidence files (blobs) live in Cloud Storage; Firestore holds metadata and storage paths (see Evidence below).

---

## JSON structures (logical)

### InspectionSession

- **id**: string (Firestore document ID)
- **tenantId**: string (partition key)
- **status**: enum `created | in_progress | completed`
- **intent**: Intent (embedded)
- **target**: Target (embedded or id ref)
- **createdAt**, **updatedAt**: timestamp
- **createdBy**: string (user id)
- **completedAt**: timestamp | null
- **recordId**: string | null (when status = completed, link to materialized record)

**Validation**: tenantId and createdBy required; status transitions created → in_progress → completed.

### Intent

- **goal**: string (natural language)
- **constraints**: object (e.g. `{ "timeAvailable": "30m", "environment": "outdoor" }`)

Embedded in InspectionSession.

### Target

- **type**: string (e.g. vehicle, property, equipment)
- **identifier**: string | null (e.g. VIN, address)
- **displayName**: string | null

Embedded or referenced by id in session.

### Step

- **id**: string
- **sessionId**: string (parent)
- **order**: number (for display/reorder)
- **type**: string (e.g. check, document, micro_flow)
- **prompt**: string (question or instruction shown to user)
- **targetId**: string | null (optional link to Target)
- **status**: enum `pending | in_progress | completed | skipped`
- **createdAt**, **updatedAt**: timestamp
- **source**: enum `initial | added | branched` (for attribution)

**Validation**: sessionId required; status transitions allowed per FR-005.

### Observation

- **id**: string
- **sessionId**: string
- **stepId**: string
- **content**: string (finding or note)
- **priority**: enum `critical | normal | low`
- **createdAt**: timestamp
- **createdBy**: string (user id)
- **evidenceIds**: string[] (references to Evidence subcollection)

**Validation**: stepId and createdBy required; priority used for relevance (FR-009).

### Evidence

- **id**: string
- **sessionId**: string
- **observationId**: string
- **type**: enum `note | photo | measurement | file`
- **storagePath**: string | null (Cloud Storage path for blobs)
- **payload**: object | null (inline text, structured measurement, etc.)
- **createdAt**: timestamp
- **createdBy**: string

**Validation**: Either storagePath (file/photo) or payload (note/measurement) present; createdBy required for attribution (FR-012).

### Collaboration

- **id**: string
- **sessionId**: string
- **type**: enum `comment | follow_up_task | evidence`
- **content**: string | object (comment text, task description, or evidence ref)
- **createdAt**: timestamp
- **createdBy**: string (participant id)
- **resolvedAt**: timestamp | null (for follow-ups)
- **linkedStepId**: string | null (suggestion applied to step)

**Validation**: createdBy required; type and content match.

### InspectionRecord (output)

- **id**: string
- **sessionId**: string
- **tenantId**: string
- **summary**: { findings: [], evidenceSummary: [], incomplete: [], followUps: [] }
- **generatedAt**: timestamp
- **version**: number (for reviewable/reversible)

Materialized when session is completed; can be stored in a separate collection or as a subcollection under the session for audit.

---

## State transitions

- **InspectionSession.status**: `created` → `in_progress` (first step started or first prompt sent) → `completed` (user or system marks complete; record generated).
- **Step.status**: `pending` → `in_progress` (user is on this step) → `completed` | `skipped`.

---

## Multi-tenancy and security

- All session-scoped documents are under `tenants/{tenantId}/inspection_sessions/...`.
- Firestore rules MUST restrict read/write by tenant and by user (e.g. creator or collaborator).
- Evidence in Cloud Storage MUST be keyed by tenantId and sessionId; rules MUST enforce tenant and session access.

# Doc updates for multiple API endpoints (main repo)

Apply these edits in the **main repo** at `specs/001-ai-guided-inspection/` (e.g. when merging this worktree or syncing specs).

## plan.md

1. In **Project Structure** > Source Code, change:
   - `└── main.py                # Function entrypoints`
   to:
   - `└── main.py                # Multiple HTTP Cloud Function entrypoints`

2. After the "Structure Decision" paragraph, add a new section:

```markdown
## API deployment

The inspection API is implemented as **multiple HTTP Cloud Functions** (one per route group). Clients call Cloud Functions directly; no Firebase Hosting rewrites are required for the API.

| Function name | Serves |
|---------------|--------|
| `inspection_sessions` | POST create session, GET session, POST complete |
| `inspection_next` | POST submit answer and get next prompt |
| `inspection_evidence` | POST add evidence |
| `inspection_record` | GET inspection record |

Each function has its own URL (e.g. `https://REGION-PROJECT.cloudfunctions.net/inspection_sessions`). The client sends the same path as in the OpenAPI contract (e.g. `/api/v1/tenants/{tenantId}/inspection_sessions`) as the request path to the appropriate function URL. Hosting can be added later to expose a single base URL if desired.
```

## quickstart.md

1. Under **Run locally**, replace the "Cloud Functions" bullet with:

```markdown
2. **Cloud Functions** (four functions: inspection_sessions, inspection_next, inspection_evidence, inspection_record):
   ```bash
   firebase emulators:start --only functions
   ```
   Or `cd functions && pip install -r requirements.txt` and run the Functions emulator. The client uses **four base URLs** (one per function) and sends the path as in the OpenAPI (e.g. `/api/v1/tenants/{tenantId}/inspection_sessions`).
```

2. Under **Key flows (for manual testing)**, replace the numbered list with:

```markdown
Use the **function URL** for each operation as the request base; send the path as below.

1. **Create session**: POST to `{inspection_sessions_url}/api/v1/tenants/{tenantId}/inspection_sessions` with body `{ "intent": { "goal": "Inspect vehicle before purchase" } }` → expect 201 and initial steps or first prompt.
2. **Next prompt**: POST to `{inspection_next_url}/api/v1/tenants/{tenantId}/inspection_sessions/{sessionId}/next` with `{ "answer": "..." }` → expect next prompt or completion.
3. **Add evidence**: POST to `{inspection_evidence_url}/api/v1/tenants/{tenantId}/inspection_sessions/{sessionId}/evidence` with observationId and type/payload or storagePath.
4. **Get record**: GET `{inspection_record_url}/api/v1/tenants/{tenantId}/inspection_sessions/{sessionId}/record` (after completion) → decision-ready summary.
```

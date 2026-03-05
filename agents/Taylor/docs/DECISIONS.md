ADR Log: LinkedIn Uploader MVP

1) Use Redis + Celery for scheduling and worker queue
- Decision: Single Redis instance as broker and short-term scheduler store; Celery for worker orchestration.
- Status: Accepted
- Rationale: Low ops overhead; Redis supports sorted sets for time-based scheduling and Celery is mature.

2) Single-tenant design
- Decision: MVP will be single-tenant.
- Status: Accepted
- Rationale: Simplifies auth, data model, and reduces scope.

3) OAuth flow + token storage
- Decision: Authorization Code flow with PKCE; store refresh tokens encrypted and rotate.
- Status: Accepted

4) Backoff & Rate-limit handling
- Decision: Exponential backoff with cap, honor Retry-After, persist retry metadata.
- Status: Accepted

Created: docs/DECISIONS.md

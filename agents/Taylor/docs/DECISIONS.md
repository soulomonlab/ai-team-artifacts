# Architecture Decisions (ADRs)

## ADR 001 — Visual Inspection App: Stack and key decisions

Date: 2026-03-06

Context
- Tablet-first PWA with offline-first capture.
- Image objects stored in S3-compatible object store; metadata and annotations in PostgreSQL.
- RBAC + enterprise SSO required; ML deferred to future sprint.

Decision
- Stack: Frontend = Next.js PWA; Backend = FastAPI; DB = PostgreSQL; Object store = S3-compatible (e.g., MinIO or AWS S3); Auth = SAML/OIDC SSO with JWT session on API.
- Offline-first: service-worker + IndexedDB for local image caching and upload queue.
- API contract: RESTful endpoints for capture/upload, metadata CRUD, sync queue, RBAC.

Consequences
- Pros: Familiar stack for team, predictable scaling, decoupled ML. Offlines requires careful conflict resolution.
- Cons: SSO integration details depend on enterprise IdP (blocking for final QA).

Alternatives considered
- Mobile native app (rejected: PWA faster to iterate). 
- Storing images in DB (rejected: performance/size concerns).

Recorded-by: Taylor (CTO)

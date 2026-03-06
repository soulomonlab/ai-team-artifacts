Project: Visual Inspection App — PoC Plan & Week-by-Week Effort Estimate

Conclusion (what I created):
- PoC plan that demonstrates offline capture, direct-to-S3 upload with presigned URLs, basic metadata CRUD, and RBAC + SSO login.
- 8-week detailed week-by-week plan mapped to team owners and deliverables.

PoC Goals (scope-limited):
- Tablet PWA that captures images offline and syncs when online
- Presigned URL flow for direct S3 uploads
- Postgres metadata endpoint with basic inspection record model
- Simple RBAC with an OIDC test IdP (Auth0 or Keycloak) integration
- Background worker for thumbnail generation
- Tests: unit tests for backend endpoints and e2e for offline->sync flow (Playwright)

Success Criteria (PoC):
- PWA can capture images offline, queue them, and successfully sync to backend when online
- Uploaded images land in S3-compatible store and metadata is persisted in Postgres
- RBAC enforced: viewer vs inspector roles tested
- Basic monitoring in place (errors + queue depth) and runbook for replaying failed syncs

Week-by-week plan (8 weeks, 8w estimate from Alex aligns)
- Week 0 (Prep, 1 week): Repository setup, CI, dev infra (minikube/Railway), initial schema, create feature/visual-inspection branch.
  - Owners: Taylor (me) for repo bootstrap; Noah for infra; Marcus initial DB schema
  - Deliverables: repo scaffold, CI pipeline, docs/ADR, empty env infra

- Week 1 (Frontend PWA skeleton + Offline storage):
  - Owners: Kevin
  - Deliverables: Next.js PWA skeleton, IndexedDB schema for images & queues, Service Worker scaffolding, capture UI mock
  - Tests: local PWA install and capture flow

- Week 2 (Auth + Presigned URL endpoints):
  - Owners: Marcus & Isabella
  - Deliverables: OIDC test IdP integration, RBAC mapping, backend endpoints for presigned URL creation, API auth middleware
  - Tests: login flow and secure presigned URL issuance

- Week 3 (Direct-to-S3 upload + backend metadata API):
  - Owners: Kevin & Marcus
  - Deliverables: client presigned PUT + confirm flow, POST metadata endpoint, DB model and migrations
  - Tests: end-to-end upload -> backend confirm

- Week 4 (Background workers + thumbnail generation):
  - Owners: Marcus/Noah
  - Deliverables: Queue infra (Redis), worker to fetch S3 objects, generate thumbnails, write derivative keys to Postgres
  - Tests: worker processes uploaded image and updates metadata

- Week 5 (Sync reconciliation + conflict handling):
  - Owners: Marcus & Kevin
  - Deliverables: client sync protocol, server reconciliation endpoint, conflict resolution policy implemented
  - Tests: offline edits, conflict scenarios

- Week 6 (Admin UI + RBAC enforcement + monitoring):
  - Owners: Kevin/Isabella/Noah
  - Deliverables: Admin console for user/role management, Prometheus + Grafana basic dashboards, Sentry integration
  - Tests: role assignment affects UI and API access; monitoring alerts

- Week 7 (QA, performance tuning, and documentation):
  - Owners: Dana & Emma
  - Deliverables: Test sweep (offline heavy-load), performance tuning, runbook for SSO & object store setup, API docs
  - Tests: SLA tests, offline sync stress tests

- Week 8 (Buffer, demo prep, handoff):
  - Owners: Alex/Taylor
  - Deliverables: Demo app, PoC validation report, handoff notes for full implementation

Risks & Mitigations:
- Risk: Enterprise SSO mapping variations across customers. Mitigation: build SSO adapter layer and test with Keycloak + Auth0.
- Risk: Large images cause device storage pressure. Mitigation: client-side compression, auto-delete after successful upload.
- Risk: Network variability on tablets. Mitigation: robust retry/backoff, chunked uploads optionally.

Open blockers to resolve before PoC start:
- Customer IdP test credentials or decision on test IdP (Auth0/Keycloak)
- Access/provisioning permissions for S3-compatible bucket
- Device fleet constraints (OS versions, browser versions)

Artifacts created:
- output/specs/feature_visual_inspection_poc_plan_and_timeline.md

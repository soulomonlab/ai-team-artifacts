Conclusion: Created GitHub issue templates / task list for repo bootstrap and initial epics. Next step is to actually create the repository and issues in GitHub (I will call create_repository and create_issue next). File contains the tasks and issue text to use when creating the repo and issues.

Repo bootstrap checklist (to run as Taylor):
1. create_repository(name='visual-inspection')
2. setup_repo_labels()
3. commit initial scaffold (README, docs/DECISIONS.md, docs/STATUS.md, docs/RUNBOOK.md, docs/ARCHITECTURE.md, .github/workflows/ci.yml, src/)
4. create branch feature/visual-inspection
5. create Epics issues (Backend API, Frontend PWA, DevOps CI/CD, QA Plan, Docs)

Issue drafts (copy into create_issue):

[Epic] Backend: API design + data models
Labels: epic, backend, P1
Body:
PRD: Implement metadata API for Visual Inspection PoC. Acceptance criteria:\n- Postgres schema for inspections, images, users, roles\n- Presigned URL endpoint for direct-to-S3 uploads\n- Sync endpoint to reconcile client queues\n- Auth hooks for OIDC SSO & RBAC enforcement\n
Deliverables:\n- API contract (OpenAPI)\n- Alembic migrations\n- Unit tests (pytest)\n
[Epic] Frontend: PWA UI + offline-first
Labels: epic, frontend, P1
Body:\nPRD: Build tablet-first PWA enabling offline image capture, local queueing, and sync. Acceptance criteria:\n- Next.js PWA skeleton with IndexedDB schema\n- Service Worker + background sync\n- Capture UI and upload confirmation flow\n- E2E tests for offline->sync

[Epic] DevOps: CI/CD + Infra
Labels: epic, devops, P1
Body:\nPRD: Provision infra for PoC: Postgres, Redis, object store, CI pipelines. Acceptance criteria:\n- Railway/AWS deployment scripts\n- GitHub Actions CI configured\n- Terraform or scripts to provision S3 bucket and IAM roles (if AWS)

[Epic] QA: Test plan + acceptance tests
Labels: epic, P1
Body:\nPRD: Define QA acceptance tests and load/perf tests for offline sync and uploads. Acceptance criteria:\n- QA test matrix covering offline scenarios, sync conflicts, and roles
- Playwright e2e scripts for critical path

[Epic] Docs: Technical docs & runbooks
Labels: epic, documentation, P2
Body:\nPRD: Create docs for ADRs, deployment runbook, SSO integration guide, and API reference.

Files produced:
- output/specs/feature_visual_inspection_repo_bootstrap_tasks_and_issues.md

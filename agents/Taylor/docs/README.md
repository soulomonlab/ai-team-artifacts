# product-mvp

MVP core product repo: onboarding + core task flows.

Stack
- Frontend: Next.js + TypeScript
- Backend: FastAPI + Python
- Database: Postgres
- Cache: Redis

Decisions (locked at kickoff)
- Postgres primary DB, Redis cache
- REST v1 with OpenAPI spec
- pre-commit + CI: lint + unit tests required on PRs

Branches
- main (protected)
- feature/init-project (work in progress)

CI: see .github/workflows/ci.yml

Docs: /docs

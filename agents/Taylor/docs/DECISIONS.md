# Architecture Decisions (ADR)

## 001 — Core Stack
- Frontend: Next.js + TypeScript
- Backend: FastAPI + Python 3.11
- Database: PostgreSQL (JSONB for flexible metadata)
- Auth: JWT (access + refresh tokens)

Rationale: Matches team expertise; Postgres JSONB provides flexible metadata while keeping relational guarantees. JWT is fastest to implement and scales for our MVP.

## 002 — Branching & CI
- Branching: feature/*, fix/* → PR into main
- Policy: Never push to main directly
- CI: GitHub Actions template with Python test run + ruff

## 003 — API
- Style: REST v1 for initial release. Evaluate GraphQL later.
- Versioning: /api/v1/
- Pagination: cursor-based for lists

## Consequences
- Early decisions favor speed-to-demo; will revisit for scale (e.g., auth provider, data warehousing).
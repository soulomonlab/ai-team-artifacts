# Architecture Decisions (ADRs)

## 1. Primary DB and Cache
Decision: Use Postgres as primary relational DB and Redis as cache/session store.
Rationale: Need strong consistency for user/task data; Redis for low-latency reads and rate limiting.
Consequences: Operational overhead for Redis; choose managed services in prod.

## 2. API
Decision: REST v1 with OpenAPI spec.
Rationale: Clear contracts for frontend; easier to iterate MVP.

## 3. Auth
Decision: JWT for session tokens; OAuth2 for third-party (future).

## 4. CI / Code Quality
Decision: pre-commit + GitHub Actions CI (lint + unit tests) required on PRs.

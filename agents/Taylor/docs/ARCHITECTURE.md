Project: MVP Architecture (Taylor — Tech Lead)

Purpose
- Deliver an intuitive MVP with backend scalability and baseline code quality.
- Meet success criteria: onboarding <2 min, API p95 <300ms, 99.9% uptime, automated test coverage >=70%.

Stack (DECIDED)
- Frontend: Next.js + TypeScript (Vercel)
- Backend: FastAPI (Python 3.11) + Postgres + Alembic
- Auth: JWT (short lived access + refresh tokens) behind HTTPS
- CI/CD: GitHub Actions -> Deploy to Railway (backend) + Vercel (frontend)
- Observability: Prometheus + Grafana (metrics), ELK or Loki (logs), Sentry (errors)

High-level components
1. API Gateway (managed by infra, e.g., Railway/Cloud load balancer)
2. FastAPI service(s) behind autoscaling group
3. Postgres primary + read replicas
4. Redis for caching sessions, rate-limiting, and short-lived data
5. Static assets via Vercel/CDN
6. Background workers (Celery/RQ) for async tasks

Key design decisions
- REST API with well-defined resource boundaries (rather than GraphQL) to simplify MVP and caching.
- Use Postgres as single source of truth; JSONB for flexible fields where needed.
- Caching layer (Redis) to meet p95 latency target and reduce DB load.
- Horizontal scaling of stateless FastAPI workers; DB vertical + read replicas for read scale.
- Instrumentation mandatory: every service must emit latency, error, and throughput metrics.

Security (baseline for MVP)
- TLS everywhere; enforce HSTS
- JWT with rotating refresh tokens and token revocation list in Redis
- Input validation on FastAPI models + ruff/mypy linting
- Automated dependency scanning in CI (dependabot + Snyk/OSV)
- Minimal IAM for infra creds; secrets in Vault/Railway secret store

Operational targets
- p95 API latency <300ms: enforce DB query budgets, cache hot paths, and use efficient indexes
- 99.9% uptime: SLA-oriented monitoring + automated restart policies + health checks
- Recovery time objective (RTO) <5m for service process restarts; RPO depends on DB setup

Next steps & owners
- #ai-backend (Marcus): implement FastAPI skeleton, DB schema, caching patterns
- #ai-devops (Noah): infra provisioning (staging), metrics + alerting baseline
- #ai-security (Isabella): threat assessment & controls
- #ai-ml, #ai-frontend as needed

Files
- output/docs/ARCHITECTURE.md

Decision log: add ADRs to docs/DECISIONS.md (I will create an ADR for REST vs GraphQL).
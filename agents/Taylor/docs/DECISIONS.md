# Architecture Decision Record (Draft)

Owner: Taylor (Tech Lead)
Date: 2026-03-06
Status: Draft — will finalize by Thu (EOD)

## Purpose
Produce final architecture decision doc for MVP: service boundaries, data model, scaling strategy, infra choices, and cost estimate.

## Key Decisions (draft)
- Primary DB: Postgres (managed). Rationale: ACID, SQL analytics, JSONB flexibility.
- Cache: Redis (managed) for low-latency reads, rate-limiting, ephemeral session store.
- Orchestration: Kubernetes (cloud-managed) for horizontal scaling and team familiarity.
- Backend framework: FastAPI (Python) — high performance, async, small team ramp.
- Frontend: Next.js + TypeScript (web) and React Native (mobile) for shared components.
- Auth: JWT + refresh tokens (short-lived access tokens). External OIDC for SSO optional.
- Infra pattern: microservices-ish (small services) behind API gateway, but keep MVP small: 3 core services (API gateway/auth, core domain service, worker/jobs) + ML service as feature flag.

## Service Boundaries (MVP)
1. API Gateway + Auth: routing, rate limits, auth checks.
2. Core API Service: user flows, business logic, Postgres primary.
3. Worker / Background Jobs: async tasks, heavy processing, use Redis queue.
4. ML Service (separate): model serving if needed; otherwise co-locate in worker for MVP.

## Data Model (high-level)
- Users: id, email (unique), profile JSONB, auth metadata
- Entities (core domain): id, owner_id, state, payload JSONB
- Events/Audit: append-only log for critical actions
- Indexing: use Postgres indexes + Redis cache for hot reads

## Scaling Strategy
- Make services stateless where possible; store state in Postgres/Redis.
- K8s HPA based on CPU/RPS and custom metrics (p95 latency alert target <200ms).
- Postgres: managed primary + read replicas. Slave for analytics and reporting.
- Redis: clustered managed instance for high availability.

## Cost Estimate Approach
- Produce two profiles: modest-dev (staging-like) and production-MVP (3-5 node k8s, managed Postgres, Redis, load balancer). Noah to finalize numbers after this doc.

## Security & Compliance (high level)
- TLS everywhere, secret management (vault/managed), IAM least privilege.
- Data retention policy and ability to redact PII.
- Isabella to produce threat model and must-have controls; we will adopt her list.

## Risks & Mitigations
- Kubernetes complexity -> use managed K8s (EKS/GKE/AKS) and Terraform + IaC templates.
- Cost > budget -> start on smaller node sizes and autoscaling.
- ML serving latency -> defer to separate service; may feature-flag until needed.

## Open Questions
- Which cloud provider? (cost vs managed services trade-offs)
- Analytics pipeline scope for MVP (simple event export vs full pipeline)

## Next Steps
- Finalize this doc by Thu EOD (I will merge updates). See file: output/docs/DECISIONS.md
- Noah: prepare IaC skeleton after final doc.
- Isabella: threat model + controls by Fri.
- Marcus: prepare API surface and initial DB schema PR after doc finalized.

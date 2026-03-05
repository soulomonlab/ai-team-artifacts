Project: Automated Marketing — LinkedIn Uploader

Overview
- Purpose: Upload approved marketing assets to LinkedIn on behalf of pilot users.
- High level: FastAPI REST backend + background workers for upload orchestration + Postgres for data + Redis as broker/cache.

Core Components
- API: FastAPI (uvicorn) exposing endpoints for OAuth flow, upload job creation, job status, and admin hooks.
- Worker: Celery (with Redis broker + result backend) handling upload jobs, retry, rate-limit backoff, token refresh.
- DB: Postgres for user, token (encrypted), job, asset metadata.
- Cache/Broker: Redis for Celery broker/results and short-lived caches.
- Auth: OAuth2 for LinkedIn (authorization_code). Encrypted tokens at rest using KMS (env-managed keys). No automated engagement actions (comment/like) per TOS.
- Infra: Containerized (Docker) + Kubernetes deployment with HPA; Prometheus + Alertmanager for metrics/alerts.

Observability
- Structured logs (JSON) + request IDs.
- Metrics: job queue length, job failure rate, token refresh failures, API latency.

Security
- Tokens encrypted with app-level KMS; rotate keys and support token revocation.
- Principle of least privilege for service accounts.

Rationale
- Celery chosen for mature scheduling/retry semantics and community support. Redis used as broker to match ops decision for Redis.
- FastAPI for quick async endpoints and good OpenAPI surface for frontend/product.

Next steps
- Create DB schema + API spec (Marcus / #ai-backend)
- Wireframes + UX flows for OAuth and job monitoring (Maya / #ai-design)
- Infra k8s manifests + Prometheus rules (Noah / #ai-devops)

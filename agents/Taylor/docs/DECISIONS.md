# Architecture Decisions (ADR)

## Decision: Use managed serverless / managed container platform for backend (initial phase)

Date: 2026-03-06

Context
- Project goals: build intuitive UX, ensure backend scalability, maintain code quality.
- Default stack: FastAPI + Postgres.
- Timeline: fast iteration for MVP, low ops overhead desired.

Decision
- For the initial phase, we will deploy the backend as managed serverless / managed containers (Railway / serverless functions). Frontend will remain on Vercel.

Rationale
- Speed: fast setup and iteration for PR previews and QA environments.
- Ops overhead: lower maintenance compared to self-managed k8s cluster.
- Scalability: managed platforms offer autoscaling sufficient for MVP and predictable growth.
- Cost: lower initial cost and operational complexity.
- Observability & CI: easier to integrate with GitHub Actions + ephemeral environments.

Consequences
- Positive:
  - Faster QA cycles (per-PR preview environments possible).
  - Less infra work for DevOps now; focus on app features and test coverage.
- Negative / Risks:
  - Potential limits for long-running/high throughput workloads; may need k8s later.
  - Vendor lock-in surface area increases (mitigate via container images and infra-agnostic config).

Mitigations / Next Steps
- Design deployments as containerized images and keep Dockerfiles / helm-free manifests so migration to k8s later is straightforward.
- Add ADR entry if we decide to migrate to k8s later and document triggers (SLA breaches, cost threshold, throughput limits).
- DevOps (Noah) to provision Railway preview environments and add a disposable Postgres pattern for CI.

Alternatives Considered
- Start with k8s (EKS/GKE): higher control and long-term scale, but significant ops overhead up-front.
- Pure FaaS (Lambda): great autoscale, but cold-starts and integration complexity with long-running FastAPI processes.

Decision Owner: Taylor (Tech Lead)

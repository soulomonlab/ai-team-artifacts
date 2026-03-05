Title: Automated Marketing App + LinkedIn Post Uploader
Branch: feature/linkedin-uploader

Goal
- MVP to let marketing teams schedule and publish LinkedIn posts for company pages and authenticated personal profiles.

MVP Scope
- User auth (OAuth 2.0) with LinkedIn, store refresh tokens securely
- Create/schedule posts (text + image), queue for background publish
- Support company pages + personal profiles
- Simple campaign dashboard (scheduled, published, failed)
- Retry/backoff, basic rate-limit handling

Out of scope (MVP)
- Auto-liking/commenting (LinkedIn TOS risk)
- Advanced post templates or AI copywriting
- Multi-channel publishing (later)

Key Decisions
- API: REST API + background worker (Celery or RQ). Branch: feature/linkedin-uploader
- DB: Postgres for relational state. Use Redis for job queue and caching.
- Tokens: Encrypted at rest; vault for production secrets (HashiCorp/Cloud KMS).
- Infra: Containerized services, K8s autoscale for workers. Noah to advise infra sizing.
- Observability: Structured logs + Prometheus metrics + alerting for publish failures.
- Security: Minimum OAuth scopes, consent flow, and privacy/GDPR data retention policy.

Deliverables & Owners
- Product spec and acceptance criteria: Alex (#ai-product) — finalize EOD
- Technical architecture & infra plan: Taylor (#ai-tech-lead) + Noah (#ai-devops) — 3 business days
- UX flows and screens: Maya (#ai-design) — wireframes in 3 days
- Growth strategy for rollout: Jessica (#ai-growth) — initial plan for pilot
- Security review (OAuth scopes, token handling): Isabella (#ai-security)
- Support & onboarding docs: Chris (#ai-support)

Success Criteria (MVP)
- Schedule and publish posts to LinkedIn company page and personal profile
- 90% publish success rate in pilot (first 100 posts)
- Secure token storage and passing security review

Next steps
1) Alex: finalize acceptance criteria by EOD and confirm pilot users
2) Taylor: propose architecture and tech stack choices in 3 days
3) Team: open branch feature/linkedin-uploader and start initial scaffold; PRs against that branch

Notes
- Compliance: Do not implement automated engagement features to avoid TOS violations.
- Timeline target: MVP in 2 sprints (4 weeks) if no major blockers.

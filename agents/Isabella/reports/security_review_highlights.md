Security Review Highlights — LinkedIn Uploader MVP

Owner: Isabella (Security)
Due: 48h

Key decisions:
- Authorization Code + PKCE for OAuth flow
- Store refresh tokens & client_secret in Vault only; access tokens in Redis with TTL
- Token rotation: rotate refresh tokens on every use; access token TTL 15min, refresh TTL 7d
- Queue + per-account rate limiting, exponential backoff + jitter, DLQ for failed deliveries

Top immediate risks (with action requests):
1) BLOCKER — LinkedIn Developer App not yet provisioned (client_id/secret). #ai-product Alex / #ai-backend Marcus please provision or request immediately.
2) BLOCKER — Legal approval needed for automated posting behaviour. Alex: escalate.
3) HIGH — Secrets in CI/CD/repos. #ai-devops Noah: ensure Vault + Snyk + secret scanning in CI before any commit with secrets.
4) MED — Rate limits & retry logic not implemented yet. #ai-backend Marcus implement queue + rate limiter.

Deliverables I'll produce next 48h:
- Detailed OAuth middleware (FastAPI) and RBAC skeleton: output/code/security/auth_middleware.py
- Security review report after code scan: output/reports/security_review_linkedin_mvp.md

If any blocker persists beyond 24h, tag me and Taylor.


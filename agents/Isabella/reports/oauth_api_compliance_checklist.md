OAuth & LinkedIn API Compliance Checklist

Owner: Isabella (Security)
Due: 48h
Context: LinkedIn v2 OAuth2 + API for automated post scheduling (single-tenant MVP).

Summary
- Goal: Secure OAuth integration and LinkedIn API compliance for MVP (connect account, schedule/publish posts).
- Scope: OAuth flow, token handling, rate-limit/backoff, API terms compliance, logging/audit, minimal PII handling.

Decisions (security):
- Use Authorization Code flow with PKCE for all clients.
- Access token lifetime: short (15 min). Refresh tokens: 7 days with rotation.
- Store long-lived secrets (client_secret, refresh tokens) only in Vault/Secrets Manager — not in DB or code.
- All traffic over TLS; redirect URIs must be pre-registered & use HTTPS.

Checklist (item, risk, mitigation, owner)

1) LinkedIn App & Permissions
- Risk: BLOCKER — no app/client credentials -> cannot integrate
- Mitigation: Create LinkedIn Developer App, request r_liteprofile, r_emailaddress, w_member_social (and any other required scopes); capture client_id/client_secret
- Owner: #ai-product (Alex) to request app OR #ai-backend (Marcus) to create
- Severity: HIGH

2) Legal review of automated posting
- Risk: BLOCKER — automated posting may violate LinkedIn or target org terms
- Mitigation: Legal to confirm acceptable automated posting, rate/behavior constraints, messaging limits; update Terms of Service and Privacy if required
- Owner: #ai-product (Alex) + Legal
- Severity: HIGH

3) OAuth Flow Security
- Risk: MED — CSRF, token theft
- Mitigation: Use state param to prevent CSRF; use PKCE; validate redirect_uri strictly; short-lived tokens; enforce same-site cookies when used; rotate refresh tokens on use
- Owner: #ai-backend (Marcus)
- Severity: MED

4) Token Storage & Rotation
- Risk: HIGH — token compromise
- Mitigation: Store refresh tokens and client_secret only in Vault; access tokens can be cached in memory/Redis with TTL; rotate refresh tokens on exchange; audit access to Vault
- Owner: #ai-devops (Noah) + #ai-backend (Marcus)
- Severity: HIGH

5) Secrets in CI/CD & Repos
- Risk: HIGH — leaked secrets
- Mitigation: .env.example only; real secrets in Vault/K8s Secrets; prevent secrets in Git history; run Snyk/TruffleHog in CI
- Owner: #ai-devops (Noah)
- Severity: HIGH

6) Rate Limiting & Retry Strategy
- Risk: MED — hitting LinkedIn limits -> account suspension
- Mitigation: Implement queue with per-account rate limiter, exponential backoff + jitter, retry cap, DLQ for manual review. Monitor 429 and apply backoff. Respect LinkedIn rate headers if provided.
- Owner: #ai-backend (Marcus)
- Severity: MED

7) Consent, Audit & Logging
- Risk: MED — non-repudiation, compliance
- Mitigation: Log user consent event with timestamp, client_id, scopes; log publish attempts, responses, and errors; retain logs per retention policy; redact PII in logs
- Owner: #ai-backend (Marcus)
- Severity: MED

8) Least Privilege & Scopes
- Risk: LOW — over-scoped app increases blast radius
- Mitigation: Request minimal scopes required for MVP; request additional scopes later if needed
- Owner: #ai-product (Alex) + #ai-backend (Marcus)
- Severity: LOW

9) Data Handling & PII
- Risk: MED — storing post content and personal data
- Mitigation: Encrypt PII at rest (DB-level AES-256), TLS in transit, document retention & deletion policy. Avoid unnecessary user profile storage.
- Owner: #ai-backend (Marcus) + #ai-devops (Noah)
- Severity: MED

10) Replay & CSRF Protection for Composer
- Risk: LOW — forged requests
- Mitigation: Require user auth for composer actions; validate JWTs; use CSRF tokens for browser flows
- Owner: #ai-frontend (Kevin) + #ai-backend (Marcus)
- Severity: LOW

11) Abuse Detection & Rate Monitoring
- Risk: MED — bulk/spam posting
- Mitigation: Monitor posting frequency, detect anomalies; set per-account limits; escalate to human review on suspicious behavior
- Owner: #ai-growth (Jessica) + #ai-backend (Marcus)
- Severity: MED

12) API Terms & Developer Policies
- Risk: HIGH — violation leads to app revocation
- Mitigation: Read LinkedIn Developer Terms; avoid automated scraping; follow brand guidelines; include unsubscribe & opt-out flows if sending messages
- Owner: #ai-product (Alex)
- Severity: HIGH

13) Security Testing
- Risk: MED — undiscovered vulnerabilities
- Mitigation: Static analysis (Bandit, Snyk), dependency scanning, run Bandit on output/code/, submit to penetration test if possible before public beta
- Owner: Isabella (Security)
- Severity: MED

Acceptance Criteria for Security Sign-off
- LinkedIn app credentials provisioned and validated
- Legal confirms automated posting permitted
- PKCE + state implemented and tested
- Refresh tokens stored in Vault + rotation working
- Rate-limiter + retry/backoff implemented with DLQ
- Logging of consent and publish events in place
- Snyk/Bandit scans run and critical issues remediated
- Security sign-off (Isabella) completed

Immediate Blockers (call out)
- LinkedIn Developer App + client_id/client_secret (cannot proceed without)
- Legal approval for automated posting behavior
- Production redirect domain for OAuth registration

Next actions (48h)
- Marcus: Implement OAuth endpoints (authorize, callback) with PKCE + state; wire Vault for token storage; add rate-limiter hooks (48h)
- Noah: Provision Vault / K8s secret integration; ensure TLS + private callback domain (48h)
- Alex: Kick off Legal review for automated posting (48h)
- Isabella: Run Bandit + dependency scans once code is up; perform security review and sign-off

References
- LinkedIn API docs: https://learn.microsoft.com/linkedin/
- OAuth 2.0 Threat Model & Security Considerations

Contact: #ai-security (Isabella)


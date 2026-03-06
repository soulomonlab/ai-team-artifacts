Threat Model — MVP (Initial)
Date: 2026-03-06
Owner: Isabella (Security)
Scope: Core MVP flows: user authentication/registration, user profile, core API CRUD (read/write of user-generated content), and backend infra (DB, caches, API gateways). Excludes third-party marketing integrations for this iteration.
Method: STRIDE applied to assets below.

Assets
- User PII (name, email)
- Authentication tokens (access + refresh)
- Database (Postgres)
- Service credentials and secrets
- Audit logs and telemetry

Top threats (summary)
1) Broken Authentication & Session Management (Spoofing / Elevation)
   - Risk: HIGH
   - Description: Long-lived or un-rotated JWTs, token theft, weak refresh flow → account takeover.
   - Mitigations (short-term):
     • Access token: JWT, expiry 15 minutes
     • Refresh token: 7 days, rotation on use, store as secure httpOnly cookie or opaque token in Redis
     • Token revocation list + logout endpoint
     • Rate-limit auth endpoints and multi-factor on high-risk flows (later)

2) Sensitive Data Exposure (Info Disclosure)
   - Risk: HIGH
   - Description: PII leaked via logs, backups, debug endpoints, misconfigured S3 buckets.
   - Mitigations (short-term):
     • TLS 1.2+ enforced for all ingress/egress
     • Encrypt DB at rest (KMS-managed keys)
     • Sanitize/redact PII from logs; ensure debug endpoints disabled in prod
     • Backup access controls and S3 bucket policies

3) Injection / Broken Access Control (Tampering / Info Disclosure)
   - Risk: HIGH
   - Description: SQL injection, insecure direct object refs (IDOR), missing server-side authorization checks.
   - Mitigations (short-term):
     • Use parameterized queries/ORM with no raw SQL
     • Add RBAC checks on server side for every sensitive endpoint
     • Automated tests for common IDOR cases

Detection & Response
- Enable structured audit logs with user-id/context for auth events
- Integrate security alerts with PagerDuty/Slack for critical events
- Weekly dependency vulnerability scan (Snyk/Trivy) and daily critical alerts

Compliance
- GDPR: data minimization, retention 90 days for non-essential PII, right-to-erasure workflow required before GA
- SOC2: ensure audit trail for admin/privileged actions

Deliverables & Timeline
- Initial threat model + critical fixes list (this file + fixes file) — created now
- Full threat model + remediation tickets + SAST/SCA results — due Friday EOD

Needs from team
- Access to repo for SAST and SCA scans (Marcus)
- Confirmation of DB and backup locations (Noah)

Decisions made (security)
- JWT access token 15m, refresh 7d w/ rotation
- Secrets via Vault (Noah) — do NOT hardcode credentials
- Enforce TLS and HTTP->HTTPS redirect at LB

Files created
- output/reports/threat_model_mvp.md
- output/reports/security_fixes_mvp.md (initial)

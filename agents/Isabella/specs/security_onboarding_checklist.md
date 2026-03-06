FTU Onboarding — Security Checklist

Purpose
- Quick security checklist for "First‑Time User Guided Onboarding (FTU Onboarding)" PRD and implementation.
- Scope: frontend onboarding UI, backend endpoints, analytics events, A/B testing.

Key decisions
- Minimize PII in analytics: use pseudonymized user IDs for events; collect only event names + metadata necessary for activation metric.
- Auth boundary must not be widened: onboarding endpoints use existing auth; no implicit elevation. Any new token flows require design review.
- A/B experiments controlled by feature flags (server-side) to avoid client-side tampering.

Checklist (must pass before merge)
1. Authentication & sessions
   - Verify onboarding endpoints enforce auth where required (JWT or session) and validate tokens server-side.
   - Short token TTL for sensitive flows; do NOT expose refresh tokens to client JS.
2. Data minimization & analytics
   - Events: avoid PII (email, full name). Use hashed/pseudonymized IDs.
   - Confirm GDPR consent captured before storing identifiable analytics.
   - Define retention window for onboarding event logs (e.g., 90 days).
3. Client-side security
   - Sanitize any user-supplied content shown in tips (prevent XSS).
   - CSP header recommended; avoid inline scripts/styles.
   - CSRF protection on state-changing endpoints (if cookies used).
4. A/B testing & feature flags
   - Server-side assignment for control/variant; include secure experiment ID + signature if client-side needed.
   - Ensure experiment exposure logging does not leak PII.
5. Backend & infra
   - Rate limiting on onboarding endpoints to mitigate abuse/DoS.
   - Audit logging for key actions (start/complete onboarding) with minimal PII.
   - Secrets: no API keys/DB credentials in code. Use env/Vault.
6. Privacy & compliance
   - Update privacy notice for event collection if needed.
   - Provide erasure path for onboarding data tied to user deletion.
7. Testing & review
   - Include security test cases in QA checklist (Dana): auth bypass, XSS, CSRF, event data leak.
   - Security quick review required if PR touches auth/analytics code (2 business days recommended).

Next steps for team
- #ai-product / Alex: place PRD in output/specs/ (I will start review once available).
- #ai-backend / Marcus: apply server-side feature flags and ensure token validation.
- #ai-frontend / Kevin: follow sanitization + CSP guidance; tag me if auth changes.
- #ai-qa / Dana: add security test cases from section 7.
- #ai-devops / Noah: ensure secrets in Vault and schedule infra spike as P2.

Contacts & SLA
- I will perform a quick security review within 2 business days after PRD + initial backend PRs are posted.
- Blocking severity (HIGH) must be fixed before merge.

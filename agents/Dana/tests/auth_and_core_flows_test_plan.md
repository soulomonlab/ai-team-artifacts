Title: Auth + Core Flows Test Plan (Template)
Path: output/tests/auth_and_core_flows_test_plan.md

1. Overview
- Owner: Dana (QA)
- Purpose: Provide a measurable, automation-first test plan for authentication and two core UX flows (signup, main dashboard).
- Goals: Ensure auth security (JWT access/refresh), correctness of signup/login flows, and dashboard data integrity.

2. Key Decisions (from PO)
- DB: Postgres (JSONB for flexible metadata)
- API: REST v1
- Auth: JWT (access + refresh tokens)

3. Acceptance Criteria (measurable)
- All critical auth flows automated and passing on CI.
- Test coverage for backend auth + core flow modules >= 90% (unit+integration).
- Automation rate for test cases >= 70%.
- No P1 bugs in staging before any internal demo.

4. Scope
- In scope: Signup, Login, Token refresh, Logout, Password reset (if in MVP), Dashboard data load, session handling.
- Out of scope (for initial template): Social login, SSO, OAuth provider integrations.

5. Test Strategy
- Methods: unit tests, integration tests, end-to-end (E2E) smoke tests, security fuzzing, load tests for auth token endpoints.
- Techniques: Equivalence partitioning, boundary analysis, decision tables, state transition testing for tokens (valid->expired->revoked).
- Environment: local CI test DB (Postgres), mock external services, ephemeral test users.

6. Risk Areas
- Token replay and theft (refresh token handling)
- Race conditions during concurrent logins / token refresh
- Missing input validation leading to injections
- Incorrectly scoped JWT claims (privilege escalation)
- DB consistency for user metadata (JSONB edge cases)

7. Test Cases (high level)
A. Signup
- TC-SS-01: Happy path new user -> 201 created, DB row exists, email normalized.
- TC-SS-02: Duplicate email -> 409 conflict.
- TC-SS-03: Input validation (too long, invalid chars) -> 400 + validation messages.
- TC-SS-04: Rate limiting for signup endpoints.

B. Login
- TC-LG-01: Correct creds -> 200 + access & refresh tokens; tokens have correct claims & expiry.
- TC-LG-02: Wrong password -> 401, no tokens issued.
- TC-LG-03: Brute-force protection (lockout or throttling).

C. Token lifecycle
- TC-TK-01: Refresh token happy path -> new access token, refresh token rotation.
- TC-TK-02: Use of expired access token -> 401.
- TC-TK-03: Use of revoked refresh token -> 401 and audit log entry.
- TC-TK-04: Reuse of refresh token after rotation -> 401 (detect replay).

D. Logout
- TC-LO-01: Logout invalidates current refresh token and stops further refresh.

E. Dashboard / Main flow
- TC-DB-01: Authenticated user -> dashboard returns 200 with expected sections.
- TC-DB-02: Authorization: user cannot access another user's data -> 403.
- TC-DB-03: Large metadata (JSONB) edge cases – payload size, null fields.

F. Security & Injection
- TC-SC-01: SQL injection attempts on auth endpoints -> sanitized or rejected.
- TC-SC-02: XSS in user metadata fields returned in dashboard -> properly escaped.

G. Concurrency & Load
- TC-LD-01: 100 concurrent token refresh requests – no DB deadlocks, acceptable latency.

8. Automation Prioritization
- Priority P0 (automate first): Signup, Login, Token lifecycle, Logout, Authorization checks on dashboard.
- Priority P1: Rate limiting, brute-force protections, large payload handling.
- Priority P2: Edge XSS/HTML sanitization tests, rare error flows.

9. Test Data & Fixtures
- Use factory fixtures for users, tokens.
- Include deterministic clocks (freeze time) for expiry tests.

10. Metrics & Reporting
- Run pytest + coverage on CI for each PR targeting backend.
- Gate: coverage >= 90% on auth/core modules before merge to main.
- Report: output/reports/qa_auth_core_summary.md (auto-generated after runs).

11. Dependencies / Blockers
- Repo + CI template (Taylor) – required to run CI tests.
- API skeleton + endpoint contracts (Marcus) – needed to write integration tests & E2E.

12. Next steps
- I will convert high-level test cases into pytest files once API contract is available.
- Immediate deliverable: this test plan template (output/tests/auth_and_core_flows_test_plan.md).
- Timeline: start implementing automated tests as soon as repo + API skeleton are available; target initial CI green for auth flows within 48h of API skeleton.

Contact / Handoff notes
- Taylor (#ai-tech-lead): need repo + CI so I can wire tests into pipeline.
- Marcus (#ai-backend): share endpoint paths, request/response schemas, and auth header schemes.


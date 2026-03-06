OpenAPI Core Flow v1 — Acceptance Test Checklist

Source: output/docs/openapi_core_flow_v1.yaml
QA Owner: Dana (Senior QA)
Date: 2026-03-06

Scope
- Endpoints: /api/v1/auth/signup (POST), /api/v1/auth/login (POST), /api/v1/auth/refresh (POST), /api/v1/primary-action (POST), /api/v1/primary-action/{action_id} (GET)
- Key parameters from spec: access token TTL=15m, refresh token TTL=7d (rotation), idempotency window=5s, rate limit=100 req/min per IP/user, signup email delivery <=60s, error format {"error":"msg","details":{}}

Acceptance Criteria (pass/fail must be explicit)
1) Signup — email delivery
   - Given valid signup payload
   - When request POST /api/v1/auth/signup
   - Then HTTP 201 and response body contains user_id and message
   - And confirmation email is delivered to test inbox within 60s
   - Evidence: mail log + message-id + timestamp
   - Automatable: yes (requires test email sink like MailHog/Mailtrap or dev webhook)

2) Login — token issuance
   - Given confirmed user credentials
   - When POST /api/v1/auth/login
   - Then HTTP 200 with access_token, token_type, expires_in (~900s), refresh_token
   - Check: expires_in within ±5s of 900 (config drift allowance)
   - Evidence: token decode (JWT exp), response JSON
   - Automatable: yes

3) Refresh — rotation semantics
   - Scenario A (happy path rotation):
     1. Login -> obtain refresh_token R1
     2. POST /api/v1/auth/refresh with R1 -> receive new access_token and refresh_token R2
     3. R1 must be invalid immediately after successful refresh (using R1 to refresh again returns 401)
     4. R2 works to refresh again until expiry
   - Check: rotation returns new refresh_token in response and previous is revoked
   - Evidence: sequence logs, 401 for R1 after rotation
   - Automatable: yes

4) Access token TTL enforcement
   - Issue access token; either check expires_in & JWT exp claim OR simulate time advance (~>15m) to ensure token rejected after TTL
   - Expected: Authorization with expired token yields 401 with error format
   - Automatable: yes (use JWT exp claim or token TTL config)

5) Primary-action — idempotency (5s window)
   - Case 1: Client sends POST with same Idempotency-Key twice within 5s
     - Expect: second request returns same result as first (same action_id/status) and no duplicate side-effect
   - Case 2: Retry after >5s with same key may be treated as new request (clarify behavior) — default acceptance: server treats >5s key as expired and processes as new request
   - Test steps: send same payload + same Idempotency-Key concurrently and sequentially; assert single persisted resource and returned response match
   - Evidence: DB state, action logs, returned action_id
   - Automatable: yes (timing-sensitive; use deterministic waits)

6) Primary-action GET
   - Given valid action_id -> GET returns 200 and PrimaryActionResponse
   - Unknown action_id -> 404 with error format
   - Automatable: yes

7) Rate limiting (429 behavior)
   - Exceed 100 req/min per IP for unauthenticated endpoints; for authenticated endpoints per-user limit
   - Expected: HTTP 429, body follows error format, and Retry-After header present (seconds)
   - Evidence: response headers and body
   - Automatable: yes (use burst/simulated clients)

8) Error format & observability
   - All non-2xx responses must match {"error":"message","details":{}}
   - Request-ID header present in responses when provided; tracing spans emitted (can be sampled)
   - Automatable: partial (check headers/body)

9) Security checks (basic)
   - Invalid Authorization header -> 401
   - Missing bearer token for protected endpoints -> 401
   - Refresh token reuse -> should be 401 (rotation enforcement)
   - Rate-limit bypass attempts -> blocked
   - Check for token leakage in logs (no full tokens in plain logs)

Test Data & Environment Requirements (action items for backend)
- Provide test environment URL or branch/PR where endpoints are deployed and stable for QA
- Provide a test email sink (MailHog/Mailtrap/SNS/webhook) and credentials OR acceptance test hook to assert email delivery timestamps
- Provide example JWT secret or a way to decode tokens OR endpoint that returns token introspection
- Clarify rate-limit headers format: do you set Retry-After? X-RateLimit-* headers?
- Clarify idempotency duplicate response semantics (which HTTP status returned for deduped retry) — acceptance assumes same 201/200 and identical body
- Clarify whether /auth/refresh accepts refresh_token in body only or supports Authorization header as well

Automated Test Plan (targets)
- Unit tests for token TTL and refresh rotation logic (mock time)
- Integration tests (pytest) for full flows: signup->email->confirm->login->refresh->primary-action
- E2E timing tests: idempotency within 5s, email <=60s, rate-limit response
- Coverage target: QA policy requires tests to be automated where possible; aim automation rate >70%

Priority & Risk Areas
- High: refresh token rotation (security), idempotency correctness (data duplication), email delivery SLA
- Medium: rate-limiting correctness, error formatting consistency

Missing / Clarification requests for Marcus (must supply before QA acceptance)
1. Provide test env/branch/PR URL and credentials
2. Provide test email sink or acceptance hook and example confirmation email payload
3. Confirm exact dedupe behavior/status code for idempotent retries (second request within 5s): return same 201 vs 409?
4. Confirm 429 response headers (Retry-After and any X-RateLimit headers)
5. Confirm refresh endpoint token format (body vs header) and whether rotated refresh token is returned in every successful refresh response

Output files
- output/reports/openapi_core_flow_v1_acceptance_checklist.md (this file)

Next steps (QA)
- Wait for Marcus to provide missing items (test env, mail sink, behavior clarifications)
- On availability: implement automated tests under output/tests/core_flow_v1/

Sign-off gate
- All checklist items green + automation coverage for critical flows (signup/login/refresh/idempotency/rate-limit) >= 70% automated


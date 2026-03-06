QA Test Plan — Quick-win MVP (E2E + Load)

Scope
- E2E flow: signup -> login -> profile update
- Auth endpoints: /signup, /login, /profile (GET/PATCH)

Objectives
- Verify correctness of auth flows end-to-end
- Ensure auth endpoints can handle expected load
- Define pass/fail criteria for release

Test types
1) E2E automated tests (pytest)
   - Happy path: signup, login, update, read
   - Token absent shapes
   - Boundary: max email length, password min/max
   - Negative: invalid email, weak password, duplicate signup
2) Load testing (locust)
   - Scenario: ramp to 200 RPS over 5 minutes, sustain 5 minutes
   - Mix: 75% signup+login+profile, 25% login-only failures
3) Security checks
   - Injection attempts in fields, CSRF headers, token replay
4) Resilience
   - Rate-limiting behavior, 429 handling

Pass criteria
- Functional: All E2E pytest tests pass against staging (exit code 0)
- Performance: 95th percentile latency < 500ms for auth endpoints at target load
- Error rate: < 1% HTTP 5xx, < 2% 4xx (except expected 401 for login-only failures)
- No P1 bugs found

Environments
- Staging (identical to prod-ish) for E2E and load
- BASE_URL env var for pytest

Automation
- Tests in output/tests/
- Locust script in output/tests/locustfile_auth.py

Execution steps
1) Run E2E: BASE_URL=https://staging.example.com pytest output/tests/test_e2e_auth.py -q
2) Run locust: locust -f output/tests/locustfile_auth.py --host=https://staging.example.com

Reporting
- output/reports/qa_quickwin_mvp_report.md will contain results and coverage

Risks & Mitigations
- Data bleed: use unique emails (qa+uuid) and garbage-collect test accounts
- DB impact: discuss with #ai-backend before high-load runs

Owner
- QA: Dana

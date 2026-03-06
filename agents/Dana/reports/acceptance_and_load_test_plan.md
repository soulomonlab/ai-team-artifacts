Title: Acceptance Criteria & Load Test Plan
Owner: Dana (QA)
Due: Next Tue (COB)

1) Overview
- Purpose: Define measurable acceptance criteria and load-test scenarios for initial API scaffold and UX flows.
- Scope: Public REST APIs, internal gRPC services (where applicable), auth flows, Redis cache, Postgres JSONB interactions.

2) Acceptance Criteria (measurable)
- Functional
  - CRUD endpoints return correct HTTP status codes and payloads per OpenAPI contract.
  - Auth: protected endpoints reject unauthenticated requests with 401; role-based access returns 403.
  - Input validation: invalid payloads return 400 with error codes.
- Non-functional
  - API response time (p95) for simple read endpoints < 200ms under baseline load.
  - Error rate < 0.1% under test scenarios.
- Security
  - No auth bypass; tokens validated; SQL injection payloads sanitized (no stack traces leaked).
- Test coverage
  - Unit+integration coverage target: >= 90% (QA recommendation). Alex/PO set target currently 85% — propose QA gate at 90%.

3) Test Matrix (happy / boundary / negative)
- Auth: valid token, expired token, malformed token, missing token, insufficient scopes.
- Data validation: required fields missing, max-length boundary, invalid types, extra fields.
- Concurrency: simultaneous writes to same resource (race condition checks).
- Cache: stale cache vs DB consistency (TTL, cache invalidation tests).

4) Load Test Plan (SLA targets & scenarios)
- Tools: k6 (preferred) + optional Locust for Python-based flows.
- Baseline SLA targets (proposal — confirm with Growth)
  - Baseline QPS: 100 req/s (initial), Peak QPS: 1,000 req/s (growth plan). If Growth provides estimate, we'll adjust.
  - Latency: p95 < 500ms at baseline; p95 < 1s at peak.
  - Error rate: < 1% at baseline; < 5% at peak.
- Scenarios
  - Scenario A (auth-heavy): 30% login/token refresh, 70% read operations.
  - Scenario B (write-heavy): 20% read, 80% write/update/delete with DB persistence checks.
  - Scenario C (spike): sudden 5x ramp in 60s to test autoscaling.
- Test shapes
  - Ramp test: ramp to baseline over 5m, hold 15m, ramp down 5m.
  - Soak test: hold baseline for 2h to detect memory leaks.
  - Spike test: 60s ramp to peak, hold 10m, monitor errors.
- Metrics to capture
  - Latency (p50/p95/p99), throughput, error rates, CPU/memory, DB connection usage, Redis hit ratio, GC pauses.
- Pass/Fail
  - Pass if SLA targets met and no P1/P2 functional/regression defects introduced.

5) Automation & Deliverables
- Files to produce:
  - output/tests/test_acceptance_api.py (pytest skeletons)
  - output/tests/k6/ (k6 scripts for each scenario)
  - output/reports/load_test_results_{timestamp}.md
- Automation targets: automate >= 70% of test cases; acceptance tests run in CI on PRs.

6) Blockers & Requests
- Marcus: confirm auth choice (JWT vs OAuth2). If OAuth2, I need details on token endpoint, refresh flow, scopes, revocation. Default assumption for test plan: JWT with expiry + refresh endpoint.
- Growth: provide expected QPS/user growth to finalize SLA targets.
- Backend: provide OpenAPI spec branch/PR (feature/api-scaffold) to generate contract tests.

7) Timeline
- Draft complete: this file (output/reports/acceptance_and_load_test_plan.md).
- Next: produce pytest skeletons and k6 scripts after feature/api-scaffold PR is available — target mid next week.

Notes:
- QA recommends raising coverage gate to 90% before prod deploy.
- Will log P1/P2 bugs as issues on discovery and notify #ai-backend immediately.

MVP Test Entry Criteria

Location: output/specs/mvp_test_entry_criteria.md

Purpose
- Provide clear, measurable entry criteria QA requires before beginning automated and manual test execution for the MVP backend/API work.

Hard entry criteria (must be met before QA starts)
1. PRD approved and available: output/specs/initial_prd.md (Taylor approval recorded).
2. OpenAPI v3 contract committed: output/docs/openapi_v1.yaml (complete for all MVP endpoints).
3. Feature branch created: feat/backend-api-prd in repo with initial stubs (APIs + DB schema). Reference PR URL or branch name in PR message.
4. Deployable test environment available (staging) mirroring prod config:
   - App server(s), Postgres, Redis, and gateway configured
   - OpenTelemetry collector reachable
   - Environment variables and secrets accessible to QA (test service account tokens)
5. Test data & accounts:
   - DB seed scripts + sample dataset for edge cases
   - Test users for each RBAC role (admin, editor, viewer) with credentials
   - Idempotency/replay test harness (to exercise Idempotency-Key behavior)
6. Authentication endpoints + JWT rotation implemented or mocked with realistic tokens (access 15m / refresh 7d) so we can run auth flows.
7. CI pipeline runs tests on PRs and supports running pytest in output/tests/ with coverage reports.
8. Performance harness available (k6 or locust) and baseline scripts for critical endpoints.
9. Security scans enabled (SAST/secret-detection) or the team accepts manual review window.
10. Acceptance criteria per endpoint defined in PRD/OpenAPI (status codes, error schema, rate-limit headers).

Soft entry criteria (recommended before QA)
- Basic observability metrics emitted (latency, error rates, traces) for staging.
- Rate-limit behavior documented (X-RateLimit headers semantics).
- Caching behavior and TTLs documented for read-heavy endpoints.

Quality gates (must be met prior to sign-off)
- Automated test coverage for new code >= 90% (project target), overall automation rate >= 70% of planned cases for MVP.
- No P1 defects open. P2s must have triage and owners.
- Performance baseline: p95 <100ms, p99 <200ms; DB queries <20ms (identify slow queries >50ms).

Deliverables QA will produce once entry criteria met
- output/tests/test_api_mvp.py (unit + integration + security checks)
- output/reports/qa_test_plan_mvp.md (test matrix, risk areas, test case list)
- Bug reports created as issues (P1/P2/P3 classification)
- Test execution report with coverage % and perf results

Risks to call out
- Incomplete OpenAPI prevents contract/integration tests.
- Missing test environment or realistic tokens blocks end-to-end flows.
- Unseeded DB prevents deterministic tests.

Next steps for backend/PO
- Marcus/Taylor: confirm repo + create branch feat/backend-api-prd and commit OpenAPI stub.
- Alex: ensure PRD at output/specs/initial_prd.md exists and has acceptance criteria per endpoint.

If these are satisfied, QA will start: create automated tests, run pytest coverage, and report results (expected start ETA: within 24h from branch+OpenAPI+staging availability).

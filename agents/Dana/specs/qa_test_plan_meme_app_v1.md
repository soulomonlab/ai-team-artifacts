# QA Test Plan — Meme App v1

Scope:
- Features: upload, edit, publish flow; feed pagination; likes & comments; moderation & reporting.
- Non-functional: performance/load (baseline: 5,000 uploads/day), resilience, security smoke tests.

Objectives (Why):
- Ensure core user flows work reliably and are intuitive.
- Prevent regressions and catch P1/P2 issues before release.
- Validate backend can support baseline load and expected peak patterns.

Acceptance criteria (measurable):
- Functional: All critical flows (upload → edit → publish → appear in feed) pass on staging.
- Automation: >=70% of test cases automated for CI. (QA target: >90% coverage for unit/integration where applicable.)
- Performance: Under baseline load (5k uploads/day), 95th percentile upload latency < 2s for 2MB images and error rate < 0.1%.
- Reliability: No P1 bugs open at release; P2s must be triaged.

Test strategy (overall):
- Automation-first: implement pytest-based integration tests + helper fixtures.
- Manual exploratory for UX, image-editor edge-cases, and moderation policies.
- Load testing with Locust or k6 on a staging environment; synthetic traffic patterns to model daily baseline and peak bursts.

Test matrix (MECE):
1) Upload / Edit / Publish flow
   - Upload image (png, jpg), oversized image (>10MB), corrupt file, network interruption during upload
   - Edit metadata (title, tags), replace image
   - Publish/unpublish flow, immediate visibility in feed
   - Acceptance: upload succeeds (201), stored URL returned, edit updates fields, publish toggles visibility

2) Feed & Pagination
   - Feed ordering (newest first), cursor vs offset pagination, limit/offset boundary values (0,1,limit,max)
   - Empty feed handling
   - Performance: feed page fetch latency under 300ms at normal traffic

3) Likes & Comments
   - Like/unlike idempotency, concurrent likes
   - Add/edit/delete comment, comment length limits, XSS in comments
   - Metrics update (counts reflect operations)

4) Moderation / Reporting
   - Report endpoint: create report, duplicate report handling
   - Moderation actions: hide/delete content, user ban flow
   - Audit trail/logging for moderation actions

5) Security & Data Validation
   - Auth required endpoints enforce authentication and rate limits
   - Input validation: SQL/NoSQL injection, content-type validation for uploads
   - File type & size enforcement, content sniffing

6) Performance & Load
   - Baseline scenario: 5,000 uploads/day ≈ 0.058 uploads/sec sustained
   - Peak scenario: 25% of daily uploads in 1-hour peak → 1,250 uploads/hour ≈ 0.347 uploads/sec
   - Concurrency sizing: assume average upload takes 2s → concurrent uploads = RPS * avg_latency
     - Peak concurrent uploads ≈ 0.347 * 2 ≈ 0.7 ~ 1 concurrent upload (low). To stress test, model bursty spikes: 200 concurrent upload workers for robustness.
   - Targets: 95th percentile latency < 2s (2MB), error rate < 0.1% under baseline; system should gracefully degrade under higher load.

Test data & environment requirements:
- Staging environment with DB reset capability and isolated test accounts.
- A test user pool (normal users, moderator, admin).
- Test image fixtures (small, medium 2MB, large 12MB, corrupted)
- Feature flags: preview mode vs production mode configurable

Automation plan:
- Implement pytest integration suite in output/tests/test_meme_app_v1.py
- CI pipeline: run fast smoke tests on PRs, full regression + load tests on merge to staging branch
- Test coverage target: >90% for backend units & integration where testable; automation rate >70% overall

Performance test plan (tools & scenarios):
- Tools: k6 (preferred) or Locust
- Scenarios:
  1) Baseline sustained: 5k uploads/day uniformly distributed over 24h
  2) Peak burst: simulate 25% of daily uploads within 1 hour
  3) Spike test: sudden 5x increase in upload attempts for 5 minutes
- Metrics to collect: latency (p50/p95/p99), throughput, error rate, CPU/memory, disk IO, DB connections

Risk & mitigation:
- Risk: Test environment differs from production (CDN, S3 etc.) → Mitigate: run load tests against environment using same storage stack or use a performance harness.
- Risk: Uploads rely on third-party CDN signing → Mitigate: provide mock signing service or test credentials.

Deliverables created by QA:
- Automation tests: output/tests/test_meme_app_v1.py
- This QA Test Plan: output/specs/qa_test_plan_meme_app_v1.md
- Pytest run output: output/reports/pytest_output_meme_app_v1.txt (generated after execution)

Next steps (action items):
- [Marcus / Backend] Provide a stable staging URL and test credentials; ensure /health endpoint exists and a test account with upload permissions.
- [Noah / DevOps] Prepare a staging environment with S3 or equivalent and capacity to run load tests.
- QA will run the automated suite, capture failures, and file bugs as needed.

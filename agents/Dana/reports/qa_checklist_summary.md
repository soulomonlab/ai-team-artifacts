QA Checklist Summary — Meme App MVP

Files created by QA (Dana):
- output/specs/qa_plan_meme_app_mvp.md
- output/tests/test_functional_meme.py
- output/tests/test_performance_meme.py
- output/tests/test_moderation_meme.py
- output/tests/test_crossplatform_meme.py

Quick checklist before QA run:
- [ ] Set STAGING_BASE_URL
- [ ] Set TEST_USER_TOKEN, TEST_OTHER_TOKEN
- [ ] Set MOD_SERVICE_URL
- [ ] Set PERF_TOOL and PERF_TEST_BUCKET for performance runs
- [ ] Provide test-data corpus in test S3 bucket

How to run:
- Run unit/functional tests: python -m pytest output/tests/ -q
- Performance: run Locust/k6 scripts configured in CI (not included)

Pass/Fail criteria (summary):
- Functional: all critical tests pass (0 failures)
- Performance: 95th percentile upload latency <1.2s, error rate <1%
- Moderation: automated filters >=95% recall on flagged corpus, false positive rate <5%
- Cross-platform: API contract identical; manual UI checks for parity

Prepared by: Dana (QA)

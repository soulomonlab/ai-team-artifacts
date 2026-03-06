# QA Plan — Meme App MVP

Situation
- Deliver a QA plan for Meme App MVP covering functional, performance, moderation, and cross-platform validation.

Complication
- App is early-stage; environment and endpoints may not be available for automated execution.
- High-risk areas: user-generated content (UGC) moderation, image upload scaling, and cross-platform parity.

Resolution (this deliverable)
- Comprehensive QA plan + pytest test skeletons that can run against a deployed environment (skips if env not present).
- Files created:
  - output/specs/qa_plan_meme_app_mvp.md
  - output/tests/test_functional_meme.py
  - output/tests/test_performance_meme.py
  - output/tests/test_moderation_meme.py
  - output/tests/test_crossplatform_meme.py
  - output/reports/qa_checklist_summary.md

---

1) Scope & Goals
- Scope: MVP features: user sign-in (assumed existing), create/upload meme (image + text), edit meme, share meme (public link + social share), view feed, basic moderation flows.
- QA goals: verify correctness, prevent P1 production regressions, provide automated regression suites, define performance SLOs for uploads at scale (10k creations/day), and ensure moderation catches high-risk content.

2) Acceptance Criteria (high level)
- Functional: All critical flows (upload/edit/share/view) pass deterministic tests in CI; no P1 regressions.
- Performance: Under 10k daily creations (peak traffic model), 95th percentile upload latency < 1.2s, error rate < 1% (5xx or 4xx), 99.9% data durability for created memes.
- Moderation: Automated filters block >= 95% of high-confidence NSFW/profanity from synthetic test set; false positive rate < 5% on curated safe set.
- Cross-platform parity: Feature parity on iOS/Android/Web for the test matrix below.
- Test coverage goal (automation): > 90% for business-critical backend code (QA to enforce via coverage reports later).

3) Risk Areas
- File storage throughput / S3 limits
- Image processing (resizing, virus/malware scanning)
- Rate-limiting / throttling under bursty uploads
- Moderation model false negatives (NSFW) or false positives
- Broken share links or social platform integration

4) Test Strategy
- Automation-first. All functional tests are automated (pytest) and run in CI against a staging environment.
- Performance tests use k6 or Locust (recommended) with a scenario that simulates 10k daily creations; DevOps to provide staging endpoints + load testing infra.
- Moderation tests: unit tests for filter rules, integration tests with the moderation microservice, and synthetic image corpora for NSFW detection.
- Cross-platform tests: combination of automated API contract tests (backend) + manual exploratory on device farm (e.g., Firebase Test Lab / BrowserStack) for UI flows.

5) Test Matrix (examples)
- Functional (automated):
  - Upload image (jpg/png/gif), small & large (<=5MB, >5MB), malformed image.
  - Add text overlays and fonts, edit text, change image, save draft, publish.
  - Share: generate public link, access without auth, share to Twitter/Facebook (link preview metadata), copy link.
  - Permissions: private vs public, owner-only edit/delete.
  - Error paths: network disconnect during upload, expired token, invalid payloads.

- Performance:
  - Scenario A (sustained): 10k creations/day ≈ 7 creations/minute average; model bursts: 1k creations over 10 minutes peak.
  - Ramp: ramp to peak over 5 minutes; sustained 10 minutes; measure latency, throughput, errors, resource usage.
  - Acceptance: 95th percentile latency < 1.2s; error rate < 1%; CPU/RAM within allocated limits.

- Moderation:
  - Automated filter tests: profanity keywords, image-based NSFW (test corpus), copyright detection (hash-based), duplicate detection.
  - Manual review flow: flagging, review queue ordering, moderator actions (remove, warn, ban), appeal path.
  - Acceptance: automated filters block >=95% of high-confidence test samples; manual queue throughput < 30s average per item.

- Cross-platform:
  - API contract tests: identical responses (status codes, payload shapes) for iOS/Android/Web clients.
  - UI tests (manual + device farm): primary flows on a matrix of OS versions and browsers (see below).

6) Test Cases (selected, detailed)
- See output/tests/test_functional_meme.py for structured pytest cases with steps & pass/fail criteria.

7) Test Data
- Synthetic images corpus (safe + flagged): store in test-data bucket. Dev to provide access.
- User accounts: test users with roles (normal_user, moderator, admin). Provide credentials or client-side token generation.

8) Environment Requirements (blocked if missing)
- STAGING_BASE_URL (e.g., https://staging.memeapp.example)
- Test-storage credentials (S3 test bucket)
- Moderation service endpoints & API keys
- Device farm credentials for cross-platform manual tests

9) Automation & CI
- Functional pytest suite runs on each PR for backend; long-running perf tests run on schedule (nightly) or on-demand.
- Test reports: pytest JUnit XML and HTML for failures; attach to PR.
- Metrics collection: upload latency histograms and error rates pushed to monitoring (Prometheus/Grafana).

10) Reporting & SLAs
- Bug severity: P1 (crash/data loss/security) fix <4h; P2 fix <24h; P3 fix <1 week.
- QA will block releases if any P1 exists or performance SLOs fail.

11) Checklist for readiness
- Staging endpoints available
- Test accounts + storage keys
- Moderation models deployed in staging
- Device farm credentials

---
References & Next steps
- Run the pytest skeletons in output/tests/; they are designed to skip if STAGING_BASE_URL not set.
- For performance runbooks, see recommendations in the Performance section and run Locust/k6 scripts (not included here).

Prepared by: Dana (QA)
Date: 2026-03-06

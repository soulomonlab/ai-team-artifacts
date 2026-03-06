# One-Page MVP Scope

Goal: Enable users to complete the core task reliably and quickly with minimal friction in an 8-week build window.
Constraints: Postgres + Redis + Kubernetes already decided. Performance target: p95 < 200ms for API search and core actions. Postpone advanced integrations and payments.

Top 5 Features (1-line rationale each)
1. Guided Onboarding (first-run task walkthrough) — reduces early drop-off and accelerates time-to-value.
2. Core Search & Task Completion Flow — make the primary user job fast and reliable (performance priority).
3. Robust Signup/Auth + Account Recovery — eliminate authentication friction and support tickets.
4. Lightweight CSV Export & Notifications (Slack webhook opt-in) — highest-value lightweight integrations requested by users.
5. In-product Help & Progress Indicators — increases visibility and reduces support load.

Key Decisions
- Prioritize end-to-end task completion, onboarding guidance, and performance/reliability for MVP.
- Target infra: Postgres + Redis + K8s. Performance target p95 <200ms.
- Defer advanced integrations and payment features to post-MVP.

3 User Flows (happy path + 2 edge cases)
A. Happy path — New user signs up, completes guided onboarding, performs a search, finishes task, exports CSV, receives Slack notification.
B. Edge case 1 — Signup fails due to email already registered: show clear state, offer account recovery, block duplicate account creation.
C. Edge case 2 — Search times out / slow response: surface retry UI, fallback to cached results, log telemetry and surface actionable error message.

Acceptance Criteria (metrics + pass/fail tests)
- Onboarding completion rate: >= 60% of new users complete guided onboarding within 5 minutes (pass = >=60% in beta cohort).
- Core task success rate: >= 80% of users complete the core task without error (pass = >=80% success across beta users).
- Performance: API p95 < 200ms for search and core task endpoints (pass = measured p95 <200ms in staging load test at 5k RPS simulated baseline).
- Reliability: Auth error rate < 0.5% post-launch (pass = <0.5% over a rolling 7-day window).
- Export/Notification delivery: CSV export success >= 99%; Slack notifications delivered >= 98%.

Pass/fail test examples
- Simulate 1000 beta users: measure onboarding completion and core task success.
- Run k6 load test on search endpoints: verify p95 <200ms at target load.
- Simulate signup collision: verify account-recovery flow appears and prevents duplicate accounts.

Rollout Plan
- Week 0: Finalize design and API contracts (Maya + Marcus)
- Week 1–4: Implement core backend + guided onboarding + auth fixes (Marcus lead)
- Week 5–6: Frontend integration, in-product help, CSV export, Slack hook (Kevin + Ryan)
- Week 7: Staging load testing, reliability fixes, QA pass (Dana)
- Week 8: Beta rollout (cohort = 200 targeted users: power users + newcomers), monitor metrics for 2 weeks

Beta Success Metrics (to graduate from beta)
- Onboarding completion >= 60%
- Core task success >= 80%
- API p95 <200ms
- Auth error rate <0.5%

Next steps
- Review & approve by Tech Lead (Taylor) and Design (Maya) by EOD Tue.
- QA checklist creation (Dana) once approved.

Spec file: output/specs/mvp_scope_onepage.md

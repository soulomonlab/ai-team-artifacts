# Feature: MVP Scope — Customer Insights
**Goal:** Deliver a minimal, high-quality 8-week MVP addressing onboarding, performance, and reliability pain points to increase first-run task completion.
**North Star Impact:** Improve core end-to-end task completion rate and reduce support tickets related to onboarding/auth by 50% within first month post-beta.
**Users:** New users (first-run onboarding) and power users impacted by search/API latency; customer success reviewing support ticket themes.
**RICE Score:** Reach=12,000 users/quarter × Impact=2 × Confidence=80% / Effort=8w = 2,400
**Kano Category:** Must-have / Performance

Top 5 features (1-line rationale each):
1. Guided First-Run Flow (onboarding wizard + contextual tips) — reduces drop-off on the first task, directly targeting highest support signal.
2. Search/API Performance Tuning (query optimization, caching via Redis, prioritized endpoints) — necessary to meet p95 <200ms and restore core task throughput.
3. Reliable Auth & Account State (improved signup/login error handling, clearer account status UI) — reduces signup/login tickets and confusion.
4. Lightweight Exports & Notifications (CSV export + Slack webhook) — low-effort, high-user-value integration requested frequently.
5. In-Product Help & Progress Indicators (progress bar + simple analytics view) — reduces support queries and helps users complete tasks.

3 user flows
- Flow A (Happy path): New user signs up → guided onboarding wizard walks through first task → completes core task → sees success screen + progress metric. (Goal: complete first task within 10 minutes)

- Flow B (Edge case: intermittent network during onboarding): Network drops during step 2 → client retries with local state saved → user resumes where they left off after reconnect; show clear retry CTA and error toast.

- Flow C (Edge case: auth/account state mismatch): User logs in but account shows incomplete state → system shows actionable account-state banner with "Resolve" flow (resend verification / re-sync) and falls back to support ticket creation if unresolved after 2 attempts.

Acceptance Criteria (metrics + pass/fail tests):
- Performance: p95 latency for core search/API endpoints < 200ms (measured over 24h load test). PASS if p95 <200ms for 24h test at 25% expected peak traffic; FAIL otherwise.
- Onboarding completion: First-run task completion rate increases from baseline by ≥40% in beta cohort. PASS if completion rate ≥ baseline+40% over 2-week beta; FAIL otherwise.
- Reliability: Signup/login error rate <0.5% (errors per successful auth) in beta. PASS if <0.5% across beta cohort; FAIL otherwise.
- Support volume: Tickets tagged onboarding/auth decrease by ≥50% vs. prior two weeks. PASS if reduction ≥50% in first month; FAIL otherwise.
- Feature correctness: CSV export contains required fields and downloads within 3s; Slack webhook delivers notification within 2s. Manual QA: 10 random exports and 5 webhook tests must succeed.

Out of Scope:
- Advanced integrations (payment, deep 3rd-party apps) and advanced analytics dashboards — postponed to post-MVP.

Success Metrics (post-launch measurement):
- Core task completion rate (primary): target +40% in beta, +60% post-rollout.
- P95 API latency: <200ms.
- Reduction in onboarding/auth support tickets: ≥50%.
- Beta NPS for new users: ≥ +30.

Rollout plan (8-week target):
- Week 0–2: Design & backend feasibility (spec finalization, API contracts, infra tuning plan). Deliverable: tech estimate and API contract.
- Week 3–6: Implementation & internal QA (implement onboarding, perf fixes, auth improvements, exports, help UI). Deliverable: feature-complete beta build.
- Week 7: Closed beta (cohort 200–500 users) for 2 weeks; monitor metrics daily; collect qualitative feedback.
- Week 8+: Evaluate beta metrics vs. acceptance criteria → if PASS, staged rollout to 20% then 100% with monitoring and rollback plan.

Beta cohort & success metrics:
- Cohort: 200–500 new users + 50 power users selected via CS. Success = PASS on at least 3 of 4 primary metrics (p95 latency, onboarding completion, auth error rate, support ticket reduction) with no critical regressions.

GitHub Issue: see Issue created by Product Owner (linked in task)

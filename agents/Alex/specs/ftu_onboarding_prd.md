# Feature: FTU (First-Time User) Onboarding
**Goal:** Increase new-user activation by guiding users through a 4-step onboarding flow that captures profile data and connects core product value.
**North Star Impact:** Improve 7-day activation rate (activation metric defined below); expected +10% relative lift.
**Users:** New users (signup in last 7 days) who haven't completed profile/setup. Primary persona: trial/new signups trying core feature.

**RICE Score:** Reach=10,000 new users/Q × Impact=1 (moderate, ~+10% activation) × Confidence=70% / Effort=4w = 1750
**Kano Category:** Performance

**Activation Metric (Product-provided):**
- Name: ftu_activation
- Definition: User fires event `ftu.completed` within 7 days of account creation.
- Success threshold (target): +10% relative lift in ftu_activation vs baseline over A/B experiment period.

**Event schema (proposed - backend to confirm):**
- event_name: `ftu.completed`
- properties:
  - user_id (string, required)
  - signup_ts (iso8601, required)
  - completed_steps (int, 0-4)
  - variant (string: control|onboard)
  - country (string)
  - device (string)

**A/B assignment method (proposed):**
- Deterministic hash on user_id into 100 buckets.
- Buckets 0-49 -> experiment (onboarding), 50-99 -> control.
- Stratification: ensure balanced assignment by country (post-check in analytics).
- Feature-flag: server-side feature flag (backend) keyed by user_id bucket.

**Acceptance Criteria:**
- [ ] PRD stored at `output/specs/ftu_onboarding_prd.md` (this file)
- [ ] API contract available for endpoints/events required (see below)
- [ ] Design wireframes for 4 onboarding steps delivered
- [ ] A/B assignment implemented server-side and feature-flag controllable
- [ ] Activation metric (`ftu_activation`) fires in analytics with correct schema
- [ ] Automated QA test cases available and passing in CI
- [ ] No performance regression: onboarding endpoints P95 < 300ms, error rate < 1%

**High-level flow & required APIs (backend to implement API contract):**
1. GET /ftu/state?user_id=... — returns current onboarding state (completed_steps, next_step)
2. POST /ftu/complete_step — body: {user_id, step_id, step_data} → updates state; triggers `ftu.step_completed` event
3. POST /ftu/complete_flow — body: {user_id, completed_steps} → marks `ftu.completed` event
4. Feature-flag API: evaluate user_id bucket -> variant

**Out of Scope:**
- Deep personalization recommendations (Phase 2)
- Mobile-native UX; mobile team will adapt endpoints

**Success Metrics (post-launch):**
- Primary: relative lift in `ftu_activation` >= 10% vs control during experiment window
- Secondary: retention (D7) lift >= 5%, decrease in time-to-first-core-action by 15%
- No significant increase in support tickets related to signup flow

**Blockers:**
- Backend: final event schema and API contract
- Analytics: confirm instrumentation and dashboards
- QA: needs event names, schema, and A/B assignment method (provided above)

**GitHub Issue:** TBD — created by Product (see linked issue)

# Feature: Canonical Activation% Definition for Growth Experiments
**Goal:** Provide a single, unambiguous definition of "activation%" used to evaluate growth landing-copy & acquisition experiments so KPI thresholds and sample-size calculations are consistent.

**North Star Impact:** Ensures experiments are comparable, instrumentation-ready, and yield reliable, actionable decisions that improve activation metric (target lift).

**Users:** Growth PMs, Experimenters, Backend/Analytics engineers, QA — use this to (a) set KPIs, (b) instrument events, (c) compute experiment results.

**RICE Score:** Reach=All experiment-exposed users per quarter (~50k) × Impact=2 × Confidence=80% / Effort=0.5w = (50,000×2×0.8)/0.5w = 160,000 (illustrative)

**Kano Category:** Must-have (for experimental validity)

## Canonical Activation% Definition (final)
Activation% = 100 × (Count of unique experiment-exposed users who complete the Activation Event within the attribution window) / (Count of unique experiment-exposed users in the denominator cohort)

- Denominator (who counts as "experiment-exposed users")
  - Primary: Unique users (user_id if available; otherwise anonymous_id) who are exposed to a variant of the experiment during the test period. Exposure = event `experiment_exposure` OR `landing_page_view` with an experiment/variant attribute present.
  - Exposure dedup rule: If a user is exposed multiple times, count them once at first exposure during the experiment period.

- Numerator (Activation Event)
  - Canonical activation event name: `activation_event` (product team to map this to real event name, e.g., `completed_onboarding_step1`, `first_upload`, or `first_successful_transaction`).
  - Activation requires the user to complete `activation_event` after exposure (see ordering rule below) within the attribution window.

- Ordering rule
  - Valid activation only if the first recorded exposure timestamp < activation_event timestamp. If activation_event occurs before exposure, it is NOT attributed to the experiment.

## Required Event Schema (payload expectations)
Every event used for experiment attribution must include these fields in the analytics payload:
- event_name (string) — e.g., `experiment_exposure`, `landing_page_view`, `signup_complete`, `activation_event`
- user_id (nullable string) — persisted when available
- anonymous_id (string) — for unauthenticated users
- variant_id (string) — experiment_id:variant_id (e.g., `growth_2026_copy_A`)
- experiment_id (string)
- timestamp (ISO8601 / epoch ms)
- session_id (optional)
- campaign/utm parameters (utm_source, utm_medium, utm_campaign) if present
- additional metadata: device, country, referrer

Event examples (names we will instrument):
- `experiment_exposure` — fired when we assign a user to a variant (should include variant_id)
- `landing_page_view` — fired on page load (include variant_id if rendered)
- `signup_complete` — fired when account creation completes (include user_id)
- `activation_event` — product-defined event marking activation

## Attribution Window(s)
- Primary window: 7 days from first exposure (recommended default).
- Secondary windows (for sensitivity analysis): 24 hours, 14 days.
- For experiments that historically have longer conversion cycles (e.g., paid onboarding), use 14d primary but document justification.

## Exclusion Rules
- Exclude internal users and teammates by: (a) test_user flag in user profile, (b) internal IP CIDR ranges, or (c) email domain allowlist. Make sure `test_user=true` is propagated in the event payload when present.
- Exclude known bots & crawlers (via user-agent or bot-listing) from the denominator and numerator.
- Exclude users who were already "activated" before first exposure: if `activation_event.timestamp < exposure.timestamp` then treat as pre-activated and omit from both numerator and denominator OR include in denominator but mark as pre-activated (recommended: omit to avoid dilution). Decision: omit pre-activated users from denominator to measure lift on non-activated users.
- Deduplicate users across devices using user_id when present; otherwise use anonymous_id. For anonymous users who later authenticate, map events to user_id if possible but ensure first exposure dedup logic remains correct.

## Statistical & KPI Guidance
- Default significance: alpha = 0.05 (two-sided). Power = 80%.
- Minimum Detectable Effect (MDE) guidance:
  - Example: baseline activation 10% → detect absolute lift of +5 percentage points (10% → 15%): required sample ≈ 700 users per variant (two-sided, α=0.05, power=0.8).
  - General formula: use two-proportion z-test for sample sizing. Growth team can request exact per-experiment numbers from Analytics.
- Target lift thresholds (recommended):
  - Minimum meaningful absolute lift: +3pp (small experiments may be noisy)
  - Preferred decision threshold for rollout: +5pp OR relative lift ≥ 10% (whichever is stronger) and statistically significant.

## Platform & Tracking Constraints
Preferred setup (recommended):
- Allocation & feature flagging: LaunchDarkly (or Optimizely if already subscribed) for consistent bucketing.
- Event collection: Segment (or server-side event pipeline) forwarding to Amplitude / Snowflake for analysis.
- Experiment analysis: Amplitude + raw event queries in Snowflake for final reporting and QA.

Hard constraints:
- Every exposure must include explicit variant_id in the event payload; otherwise the user should be treated as unassigned and excluded from experiment calculations.
- Server-side exposures must also emit `experiment_exposure` to ensure cross-device attribution.

## Acceptance Criteria
- [ ] Spec file created and approved by Growth PM (Jessica).
- [ ] Event names and payload schema agreed and added to the instrumentation backlog.
- [ ] Backend/Analytics can map `activation_event` to the product event we want (confirm real event name).
- [ ] Sample-size calc template provided (alpha, power, baseline) and example for baseline=10%.

## Out of Scope
- Implementation of the event instrumentation (backend/analytics work).
- Post-experiment causal analysis beyond the primary activation metric (e.g., retention uplift analysis).

## Success Metrics
- Experiments use this canonical definition in 100% of growth A/B analyses for the quarter.
- Instrumentation passes QA (no missing variant_id) in the first run for ≥95% of exposures.

**Next procedural step (for implementers):** Map `activation_event` to the concrete product event name and implement `experiment_exposure` + variant_id payload fields for both client- and server-side exposures.

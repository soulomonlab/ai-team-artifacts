# Prelaunch Revenue Plan + 2 Acquisition Channel Tests

Owner: Jessica (Growth)
Date: 2026-03-06

Summary
- Deliverable: MRR baseline + 3-scenario forecast to launch + 3 months; two acquisition channel experiments; instrumentation & tracking plan; pricing experiment notes.
- Files: output/reports/prelaunch_revenue_plan.md, output/specs/experiment_paid_social.md, output/specs/experiment_partnership.md, output/specs/instrumentation_tracking_plan.md

1) MRR Forecast (Launch = month 0, then month 1–3)
Assumptions (explicit & reversible):
- Launch traffic (to landing + product): baseline 10k unique/mo, optimistic 25k, pessimistic 5k
- Landing → signup conversion: baseline 6%, opt 9%, pess 3%
- Activation (engaged, eligible for trial): 70% of signups across scenarios
- Signup → paid conversion (after trial/activation): baseline 4%, opt 6%, pess 2%
- ARPU (monthly revenue per paying user): baseline $25, opt $30, pess $20
- Monthly churn among payers: baseline 6% (LTV months ≈ 1/0.06 ≈16.7), opt 4%, pess 10%

Scenarios (numbers rounded)
- Baseline:
  - Launch (month 0): traffic 10k → signups 600 → paid conversions (4% of signups*activation) ≈ 17 paying → MRR ≈ 17 * $25 = $425
  - Month 1: traffic +10% (campaign build) → 11k → signups 660 → new paying ≈ 19 → cumulative paying (accounting churn small) ≈ 35 → MRR ≈ 35 * $25 = $875
  - Month 2: traffic +20% → 12k → signups 720 → new paying ≈ 20 → cumulative paying ≈ 53 → MRR ≈ $1,325
  - Month 3: traffic +30% → 13k → signups 780 → new paying ≈ 22 → cumulative paying ≈ 75 → MRR ≈ $1,875

- Optimistic:
  - Launch: traffic 25k → signups 2,250 → new paying ≈ 95 → MRR ≈ 95 * $30 = $2,850
  - M1: traffic 30k → signups 2,700 → new paying ≈ 108 → cumulative ≈ 200 → MRR ≈ 200 * $30 = $6,000
  - M2: traffic 40k → signups 3,600 → new paying ≈ 144 → cumulative ≈ 340 → MRR ≈ $10,200
  - M3: traffic 50k → signups 4,500 → new paying ≈ 180 → cumulative ≈ 520 → MRR ≈ $15,600

- Pessimistic:
  - Launch: traffic 5k → signups 150 → new paying ≈ 2 → MRR ≈ 2 * $20 = $40
  - M1: traffic 5.5k → signups 165 → new paying ≈ 3 → cumulative ≈ 5 → MRR ≈ $100
  - M2: traffic 6k → signups 180 → new paying ≈ 3 → cumulative ≈ 8 → MRR ≈ $160
  - M3: traffic 6.5k → signups 195 → new paying ≈ 4 → cumulative ≈ 12 → MRR ≈ $240

Key decision: use conservative baseline assumptions (traffic 10k, signup 6%, paid conversion 4%, ARPU $25). These are reversible and will be updated once first 2 weeks of launch data arrive.

2) Two acquisition channel tests (testable specs)
A. Paid Social (Meta + X)
- Objective: Acquire early users fast to validate funnel and pricing.
- Budget: $10,000 over 4 weeks (initial test)
- Targeting: lookalike of similar-product buyers + interest-based (top-converting segments)
- Expected CAC: baseline $80, optimistic $50, pessimistic $140
- LTV assumptions: ARPU $25, churn 6% → LTV ≈ $417 (gross LTV), conservative marketing LTV = $200 after costs
- Success metrics (success threshold): CAC <= $150 and 3% paid conversion among acquired cohort within 30 days
- Sample size / min signal: aim for 100 paid conversions (power for early signal). With expected CAC $80, budget $8k to reach this—fits $10k budget.
- Duration: 4 weeks
- Experiment variants to run: (1) CTA: Free trial vs Sign-up + immediate discount; (2) Landing: short-form vs long-form
- File: output/specs/experiment_paid_social.md

B. Partnerships / Creator Referrals
- Objective: Low CAC channel via partner endorsements (affiliate split)
- Budget: $5,000 (partner incentives + ops) initial 6 weeks
- Mechanics: sign partnership with 3 micro-influencers / newsletters on rev-share 20% on first payment or $20 flat per paying signup
- Expected CAC: baseline $40 (with $20 flat), optimistic $20, pessimistic $120
- LTV assumptions: same ARPU $25 (higher retention expected from quality referrals) → LTV conservatively $300
- Success metrics: CAC <= $60; >= 30 paying users from partners in 6 weeks; payback period < 3 months
- Measurement: track partner_id in signup properties and cohort performance
- File: output/specs/experiment_partnership.md

3) Instrumentation & Tracking Plan (events, cohorts, attribution)
See separate spec for implementation (output/specs/instrumentation_tracking_plan.md). High-level:
- Required events (frontend → backend analytics):
  - page.view {page_name, url, utm_source, utm_medium, utm_campaign}
  - signup.started {method, variant, partner_id, utm_*}
  - signup.completed {user_id, plan_choice, price, experiment_id}
  - activation.completed {user_id, activation_type}
  - trial.started {user_id, trial_length}
  - subscription.created {user_id, plan, price, billing_cycle, payment_method}
  - payment.succeeded {user_id, amount, currency}
  - referral.sent {user_id, channel}
  - experiment.exposed {user_id, experiment_id, variant}
- Properties to capture: utm_source/medium/campaign, referrer, partner_id, experiment_id, cohort_date, price_plan, trial_length
- Attribution model: primary = last non-direct click within 30 days; store original_utm and last_utm
- Cohorts to create: acquisition_cohort (by utm_source), partner_cohort (by partner_id), experiment_cohort (by experiment_id), paid_cohort (by first_payment_date)
- Key funnels: visit → signup → activation → trial → paid (measure conversion rates at each step by source & variant)
- Tracking tech: send events to Segment (server + client), mirror to Mixpanel/Amplitude + raw events to data warehouse (BigQuery) for SQL cohorts

4) Pricing experiments & required product/UX changes
- Suggested A/B pricing tests:
  1) Free trial (14 days) vs reduced-price trial (50% first month)
  2) Monthly $25 vs Monthly $20 (price elasticity) with anchoring (show annual $240 as default)
  3) Add ‘Starter’ lower-priced plan at $9/mo to test top-of-funnel expansion
- Success metrics per test: trial→paid conversion lift >= +20% (relative) and payback <= 3 months
- Required product/UX changes:
  - Add pricing page variants (copy + price) and experiment flagging
  - Add coupon/discount flow and analytics hook
  - Modal for upgrade with personalized LTV messaging in onboarding
  - Backend: support multiple pricing plans, promo codes, and trial length field in subscription API

5) Risks & Mitigations
- Risk: Paid Social CAC higher than forecast → mitigation: pivot budget to partnerships and content; enforce early stop criteria (if CAC > $200 after 1k clicks)
- Risk: Instrumentation gaps → mitigation: create minimal event contract and smoke tests, QA before launch

6) Next actions (growth-owner)
- Execute acquisition tests at launch T0
- Collect first 14-day cohort data and re-run forecast
- Coordinate instrumentation implementation with Backend (Marcus) and Frontend (Kevin)

Decision log (key choices)
- Use conservative baseline conversion 4% paid conversion to avoid overforecasting (reversible)
- Prioritized Paid Social + Partnerships as channel tests: paid for speed, partnership for CAC efficiency


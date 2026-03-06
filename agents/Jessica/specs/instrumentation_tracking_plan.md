# Instrumentation & Tracking Plan for Launch

Owner: Jessica (Growth)
Date: 2026-03-06

Purpose
- Provide a minimal, testable event contract to measure acquisition → activation → revenue funnel, CAC → LTV, and experiment performance.

Event contract (client + server)
1) page.view
  - properties: page_name, url, referrer, utm_source, utm_medium, utm_campaign, ad_id
2) ad.click
  - properties: ad_id, campaign, creative_id, utm_*
3) experiment.exposed
  - properties: experiment_id, variant
4) signup.started
  - properties: method, experiment_id, partner_id, utm_*
5) signup.completed
  - properties: user_id, plan_choice, price, experiment_id, partner_id, cohort_date
6) activation.completed
  - properties: user_id, activation_type
7) trial.started
  - properties: user_id, trial_length
8) subscription.created
  - properties: user_id, plan, price, billing_cycle, partner_id, coupon_code
9) payment.succeeded
  - properties: user_id, amount, currency, payment_method
10) referral.sent
  - properties: user_id, channel, referral_id

Attribution & Cohorting
- Store original_utm (first touch) and last_utm (last non-direct) on user profile
- Attribution rule: last non-direct click within 30 days
- Cohorts: acquisition_cohort (by original_utm), partner_cohort (by partner_id), experiment_cohort (by experiment_id), paid_cohort (by first_payment_date)

Delivery
- Use Segment client + server to collect events; forward to Mixpanel/Amplitude for product analytics and to BigQuery for raw events
- Provide a SQL starter query for paid_cohort LTV and CAC calculation in data folder (next deliverable)

QA
- Smoke tests: validate event payload shapes, required fields non-null, and sample user flows end-to-end before launch

Next steps
- #ai-backend (Marcus): implement server-side ingestion and persist partner_id, experiment_id, original_utm on user records
- #ai-frontend (Kevin): send experiment exposures, utm parsing, and send signup events with properties


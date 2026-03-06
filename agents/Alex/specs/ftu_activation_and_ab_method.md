FTU Activation Metric & A/B Assignment Method

Purpose
- Provide QA and Analytics the definitive activation metric and experiment assignment method for FTU onboarding tests.

Activation Metric
- Metric Name: ftu_activation
- Definition: A user is "activated" if they emit event `ftu.completed` within 7 days of account creation.
- Inclusion: users with account created during experiment window; exclude internal/bot traffic via ip_allowlist or user flag `is_internal=true`.
- Attribution window: 7 days post signup_ts.
- Denominator: unique new users who signed up during experiment window.
- Numerator: unique users satisfying activation definition within attribution window.
- Edge cases: account merges — use earliest signup_ts; multi-device — dedupe by user_id.

Event schema (final to be confirmed by Backend)
- Event: ftu.completed
  - user_id (string) — required
  - signup_ts (iso8601) — required
  - completed_steps (integer) — required
  - variant (string) — control|onboard — required
  - country (string)
  - device (string)
  - experiment_id (string) — e.g., ftu_onboard_v1
- Event: ftu.step_completed
  - user_id, signup_ts, step_id (int), step_name (string), variant

A/B Assignment & Feature-flag Method
- Deterministic assignment: hash(user_id) % 100 → bucket (0-99)
- Assignment: buckets 0-49 => onboard (50%); 50-99 => control
- Implementation: server-side feature flag service evaluates bucket for user_id; flag value = variant
- Rollout plan: start with 10% (buckets 0-9), increase by 10pp every 3 days after smoke tests
- Exposure logging: log assigned bucket and variant on user creation and in ftu.* events
- Stratification: verify balance by country and device in analytics post-hoc

QA Notes
- QA requires Backend to confirm the final event property names and provide example payloads
- QA will implement tests once PRD + API contracts are available

Owners
- Product (Alex): owner of PRD and metric definition
- Backend (Marcus): confirm schemas and implement feature-flag
- QA (Dana): create automated tests after API contract

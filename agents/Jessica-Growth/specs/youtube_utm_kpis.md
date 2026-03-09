YouTube UTM - KPI Definitions and Measurement Guidance

Purpose
- Define clear, implementable KPI definitions for measuring YouTube-driven traffic and conversions. These definitions align with existing SQL provided (output/code/youtube_utm_dashboard.sql) and are designed to be unambiguous for BigQuery/Looker/Mixpanel implementation.

Primary KPI (North Star)
- New users from YouTube (MTD and WoW)
  - Definition: Unique users whose first_seen date (canonical column user_first_seen OR derived from earliest event timestamp in events table) falls within the metric time window AND where the session/first-attribution has utm_source = 'youtube' (see attribution rules below).
  - Why: Measures top-of-funnel acquisition attributable to YouTube.

Secondary KPIs
- Sessions from YouTube
  - Definition: Count of session_start (or equivalent session identifier) where utm_source = 'youtube' on the session (or fallback referrer indicates youtube.com).
- Conversion events (YouTube-attributed)
  - Definition: Count of users who performed at least one event from the conversion set (see below) within a 14-day window from first YouTube session (or within the selected analysis window), attributed to YouTube.
- Conversion rate
  - Definition: Conversions / New users (or conversions / sessions, specify per tile) for YouTube-attributed traffic.
- 7-day retention (YouTube cohort)
  - Definition: Percentage of YouTube-new-user cohort that returned and had at least one session/event on day 7 after first_seen.

Conversion Event Set (recommended canonical names)
- signup_complete (user completed account creation)
- activation_event (first key activation step, e.g., completed onboarding step X)
- purchase / subscription_purchase (monetization events)
- upgrade (free->paid upgrade event)
- Notes: Use canonical event names from events table/event taxonomy. If your system has different event names, map them here.

Attribution Rules
- Primary attribution: utm_source param on the session / traffic source where utm_source = 'youtube'.
- Fallback: If utm parameters are missing, use referrer host contains 'youtube.com' OR campaign/medium fields indicating youtube.
- Normalization: Lowercase utm_source/utm_medium/utm_campaign values; trim whitespace.
- First-touch vs. last-touch: Dashboard will use session-level first-touch (first YouTube session for new users). If product team prefers last-touch, mark as alternative view.

New User Definition (explicit)
- Preferred (accurate): user_first_seen (canonical column on user/profile table) falling within date range.
- Acceptable fallback (if canonical not available): derive earliest event_timestamp per user from events table and use that as first_seen. Documented in SQL as a subquery (see output/code/youtube_utm_dashboard.sql).
- Edge cases: For anonymous sessions without persistent user_id, treat them as sessions only; only count as new user if user_id later materializes and first_seen falls in window.

Windowing and Timeframes
- Default tiles: MTD (Month-to-date), WoW (week-over-week), 7/14/30-day lookbacks.
- Use event timestamp's date for windowing. For MTD comparisons, calculate current MTD vs prior MTD (same number of days).

Data Quality Notes (must confirm with Engineering)
- Confirm actual events table path (replace placeholder project.dataset.events) and whether utm fields are in event_params (nested) or top-level columns.
- Confirm presence of canonical user_first_seen column (recommended). If absent, schedule a dbt model to materialize it.

Reporting Requirements
- Each dashboard tile must show raw count, percentage change vs prior period, and p-value for major experiments (where applicable).
- All metrics must be filterable by utm_campaign, utm_medium, utm_content, country, and device.

Acceptance Criteria
- Unambiguous metric definitions in this document.
- Confirmed events table path & storage details from Backend (Marcus).
- Dashboard tiles specified and SQL-ready for Looker / BI implementation.

Files referenced
- SQL: output/code/youtube_utm_dashboard.sql
- Filters spec: output/specs/youtube_utm_filters.md

Next steps (for Engineering)
- Provide actual events table path and confirm whether UTM values are top-level columns or nested in event_params; confirm canonical user_first_seen availability.

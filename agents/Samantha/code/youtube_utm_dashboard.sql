-- output/code/data/youtube_utm_dashboard.sql
-- BigQuery SQL: Sessions, New Users, Conversions (signup, trial_start, purchase)
-- Filter: utm_source = 'youtube'
-- Supports: Daily breakdown + WoW and MTD comparisons

-- PARAMETERS (set when running / in Looker or via scheduled query):
-- @current_start DATE, @current_end DATE

WITH events AS (
  SELECT
    user_id,
    session_id,
    event_name,
    DATE(event_timestamp) AS event_date,
    event_timestamp,
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key='utm_source') AS utm_source
  FROM `project.dataset.events`  -- <-- REPLACE with your events table
  WHERE DATE(event_timestamp) BETWEEN @current_start AND @current_end
    AND (SELECT value.string_value FROM UNNEST(event_params) WHERE key='utm_source') = 'youtube'
),

-- Define conversions
conversions AS (
  SELECT * FROM events
  WHERE event_name IN ("signup", "trial_start", "purchase")
),

-- Sessions: count distinct session_id per day
daily_sessions AS (
  SELECT
    event_date,
    COUNT(DISTINCT session_id) AS sessions
  FROM events
  GROUP BY event_date
),

-- New users: users whose first event (ever in full events table) falls in the window
-- This requires access to full user first_seen date. If not available, approximate by first event in events table.
first_seen AS (
  SELECT
    user_id,
    DATE(MIN(event_timestamp)) AS first_seen_date
  FROM `project.dataset.events`  -- full event table (not filtered)
  WHERE (SELECT value.string_value FROM UNNEST(event_params) WHERE key='utm_source') = 'youtube'
  GROUP BY user_id
),

daily_new_users AS (
  SELECT
    e.event_date,
    COUNT(DISTINCT e.user_id) AS new_users
  FROM events e
  JOIN first_seen f ON e.user_id = f.user_id
  WHERE f.first_seen_date = e.event_date
  GROUP BY e.event_date
),

-- Daily conversions
daily_conversions AS (
  SELECT
    event_date,
    event_name,
    COUNT(DISTINCT CONCAT(user_id, '-', CAST(event_timestamp AS STRING))) AS events_count,
    COUNT(DISTINCT user_id) AS users_converted
  FROM conversions
  GROUP BY event_date, event_name
),

-- Aggregate current period totals
agg_current AS (
  SELECT
    'current' AS period,
    COUNT(DISTINCT session_id) AS sessions,
    COUNT(DISTINCT CASE WHEN f.first_seen_date BETWEEN @current_start AND @current_end THEN e.user_id END) AS new_users,
    SUM(CASE WHEN event_name = 'signup' THEN 1 ELSE 0 END) AS signup_events,
    SUM(CASE WHEN event_name = 'trial_start' THEN 1 ELSE 0 END) AS trial_start_events,
    SUM(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchase_events
  FROM `project.dataset.events` e
  LEFT JOIN (
    SELECT user_id, DATE(MIN(event_timestamp)) AS first_seen_date
    FROM `project.dataset.events`
    GROUP BY user_id
  ) f ON e.user_id = f.user_id
  WHERE DATE(e.event_timestamp) BETWEEN @current_start AND @current_end
    AND (SELECT value.string_value FROM UNNEST(e.event_params) WHERE key='utm_source') = 'youtube'
),

-- Aggregate previous period (for WoW comparison) -- previous period same length immediately before current_start
agg_prev AS (
  SELECT
    'prev' AS period,
    COUNT(DISTINCT session_id) AS sessions,
    COUNT(DISTINCT CASE WHEN f.first_seen_date BETWEEN DATE_SUB(@current_start, INTERVAL DATE_DIFF(@current_end, @current_start, DAY)+1 DAY) AND DATE_SUB(@current_start, INTERVAL 1 DAY) THEN e.user_id END) AS new_users,
    SUM(CASE WHEN event_name = 'signup' THEN 1 ELSE 0 END) AS signup_events,
    SUM(CASE WHEN event_name = 'trial_start' THEN 1 ELSE 0 END) AS trial_start_events,
    SUM(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchase_events
  FROM `project.dataset.events` e
  LEFT JOIN (
    SELECT user_id, DATE(MIN(event_timestamp)) AS first_seen_date
    FROM `project.dataset.events`
    GROUP BY user_id
  ) f ON e.user_id = f.user_id
  WHERE DATE(e.event_timestamp) BETWEEN DATE_SUB(@current_start, INTERVAL DATE_DIFF(@current_end, @current_start, DAY)+1 DAY) AND DATE_SUB(@current_start, INTERVAL 1 DAY)
    AND (SELECT value.string_value FROM UNNEST(e.event_params) WHERE key='utm_source') = 'youtube'
)

SELECT * FROM agg_current
UNION ALL
SELECT * FROM agg_prev;

-- Notes:
-- 1) Replace `project.dataset.events` with your project/dataset.table (GA4 / Firebase or custom events table).
-- 2) If you store utm parameters as top-level columns (utm_source), simplify WHERE utm_source = 'youtube'.
-- 3) For MTD: set @current_start = DATE_TRUNC(CURRENT_DATE(), MONTH), @current_end = CURRENT_DATE() - 1
-- 4) To create daily timeseries, query daily_sessions, daily_new_users, daily_conversions CTEs instead of aggregates above.

-- output/specs/youtube_utm_filters.md

YouTube UTM Dashboard: Filter & Segment Definitions

Purpose
- Define exact SQL/segment filters to be used in Looker/Mixpanel to isolate YouTube-origin traffic.

Key fields (common naming across platforms)
- utm_source (string): expected value 'youtube' (case-insensitive)
- utm_medium (string): e.g., 'organic', 'cpc' (optional filter)
- utm_campaign (string): campaign name (optional)
- traffic_source (object / nested): GA4-specific object containing source/medium
- event_name (string): e.g., 'session_start', 'signup', 'trial_start', 'purchase'

SQL Filter (BigQuery / GA4 events table)
- WHERE LOWER((SELECT value.string_value FROM UNNEST(event_params) WHERE key='utm_source')) = 'youtube'
- AND event_name IN ('session_start', 'signup', 'trial_start', 'purchase') -- as needed

Mixpanel Segment Definition
- Filter: utm_source equals 'youtube' OR (referrer contains 'youtube.com')
- Events to include: 'session_start' or 'page_view' for sessions; conversion events: 'signup', 'trial_start', 'purchase'
- Timeframe: Last 7 days / MTD / Custom

Looker (LookML) Segment / Explore
- Create a dimension: youtube_source: sql: LOWER(${TABLE}.utm_source) = 'youtube' ;
- Use filters in dashboard tiles: youtube_source = yes

Edge cases / Data quality notes
- UTM params missing: sessions with no utm_source should be excluded. Consider adding a fallback using referrer parsing.
- Case sensitivity and leading/trailing spaces: normalize with LOWER() and TRIM().
- Cross-device attribution: if user first touched via YouTube on another device, first_seen attribution may differ.

Acceptance criteria
- Dashboard shows sessions, new users, signups, trial_starts, purchases filtered to utm_source = 'youtube'
- WoW comparison: previous period (same length) visible alongside current period
- MTD comparison: month-to-date vs prior month-to-date
- Provide SQL and segment definitions (this doc + SQL file)

Next: Coordinate with #ai-growth (Jessica) to confirm KPI definitions and dashboard access.

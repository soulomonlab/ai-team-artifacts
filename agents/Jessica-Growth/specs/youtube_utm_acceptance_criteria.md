YouTube UTM Dashboard — Acceptance Criteria

Purpose
- Concrete checklist for QA and engineering before marking the YouTube UTM dashboard task complete.

Data and SQL
- SQL (output/code/youtube_utm_dashboard.sql) runs without errors after table path replacement.
- utm_source = 'youtube' filter correctly isolates YouTube traffic, with referrer fallback working.
- New users correctly calculated using canonical user_first_seen if available; fallback earliest event logic matches the KPI doc.
- Conversion event set mapped correctly to event names in the events table.

Dashboard Functionality
- Tiles listed in output/specs/youtube_utm_dashboard_tiles.md implemented.
- Each tile supports filters: utm_campaign, utm_medium, utm_content, country, device, and date range.
- MTD/WoW comparisons and % change display correctly.

Quality
- Data normalization (lowercasing/trimming utm values) applied.
- Edge cases: missing utm params, anonymous users, and bot traffic handled or documented.

Documentation
- KPI definitions: output/specs/youtube_utm_kpis.md
- Filters spec: output/specs/youtube_utm_filters.md (created by Samantha)

Sign-off criteria
- Marcus confirms events table path and column structure.
- Dashboard tiles tested in staging and verified against raw query results by Data/Analytics.
- Acceptance sign-off by Alex (Product) and Samantha (Data).

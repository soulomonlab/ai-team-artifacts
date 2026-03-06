# YouTube Channel Setup & Growth Integration

Summary
- Deliverable: Create & verify brand YouTube channel, upload trailer, add About, link site, setup UTM tracking and analytics dashboard, define CTAs for frontend implementation.

Decisions (key)
- Attribution: Use UTM-based attribution (utm_source=youtube, utm_medium=video, utm_campaign={campaign}, utm_content={cta}) to keep GA4 + Mixpanel consistent and reversible.
- Analytics stack: Track with GA4 + Mixpanel (events) and BigQuery export for dashboarding. This is reversible and supports funnel/cohort analysis.
- CTA approach: Embed trailer on landing + persistent header CTA. Primary CTA should be "Start free" with UTM; secondary CTA = "Subscribe" (YouTube) without UTM.

Channel creation checklist
1. Create Brand Account and channel name: <BRAND_NAME>
2. Verify channel via business/phone verification
3. Upload trailer video: filename trailer_01.mp4
4. Fill About: 2-line mission, website link, contact email
5. Link website in About and channel settings (add site URL)

UTM naming conventions (mandatory)
- utm_source=youtube
- utm_medium=video
- utm_campaign=channel_trailer_v1 (change name per experiment)
- utm_content=cta_top | cta_footer | video_overlay
Example CTA link: https://our-site.com/?utm_source=youtube&utm_medium=video&utm_campaign=channel_trailer_v1&utm_content=cta_top

Tracking & events (required)
- Track these events in frontend/analytics:
  - youtube_cta_click {properties: video_id, cta_location, utm_campaign, user_id}
  - youtube_embed_play {properties: video_id, play_time_sec, user_id}
  - youtube_trailer_view (for server-side analytics via page view)
- Send events to Mixpanel and GA4. Mirror event names in both systems for crosswalk.

Dashboard & KPIs (Growth)
- Metrics to expose: clicks->site (UTM), sessions from YouTube, signup rate from YouTube sessions, 7d retention, LTV (if available)
- Minimum dashboard: YouTube Sessions (GA4), UTM campaign conversions (Signups, Paid), youtube_cta_click CTR
- Suggested timeframe: rolling 7/30/90 days

Trailer upload checklist
- Title: 6-8 words with primary keyword
- Description: First 1-2 lines include site URL with UTM link; full description with timestamps, CTA, and contact
- Thumbnail: 1280x720, readable at 256px
- Cards/end-slate: Add 1 card linking to site (use UTM) and end-slate CTA to subscribe
- Subtitles: English + primary market

Coordination notes for Frontend (Kevin)
- Embed YouTube trailer on homepage and /about
- Add header CTA using UTM link defined above
- Push analytics events: youtube_cta_click, youtube_embed_play (see properties)

Files created
- output/specs/youtube_channel_setup.md
- output/code/growth/youtube_analytics.py

Next steps
- Growth (Jessica): finalize UTM and dashboard spec (this file)
- Frontend (Kevin): implement CTAs & tracking (handed off via task)

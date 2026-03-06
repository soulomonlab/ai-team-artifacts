Title: YouTube Channel Launch — Promotion Plan

Reference: PRD → output/specs/youtube_channel.md (GitHub Issue #92)

Objective
- Support PRD goals: 5k subs, 50k views in 3 months; CTR >1.5%.

Primary KPIs
- Subs (goal: 5,000 in 90 days)
- Views (goal: 50,000 in 90 days)
- Video CTA CTR (baseline >1.5%)
- Traffic conversion funnel: visit→video click→subscribe

Timeline
- Pre-launch (2 weeks): teaser posts, email to beta users, add banner placeholders
- Launch week: hero banner, 1st email + social push, community AMA
- Ongoing (90 days): weekly highlights, paid social spikes, feature anniversaries

Channels & Tactics
- Product UI: homepage hero, in-app banner, onboarding modal (A/B test CTA copy)
- Email: segmented launch blast (power users, early adopters), weekly highlight series
- Organic Social: LinkedIn, X, Product Hunt follow-up (assets + copy kit)
- Community: Discord/Slack AMA, feature highlight threads
- Paid: targeted YouTube/Meta for weeks 1 & 4 if organic underperforms

Assets Needed
- From #ai-design (Maya): banner, avatar, thumbnail template (Figma + exported PNG/JPG sizes), accessibility notes, thumbnail text rules — Task #103
- Video files & descriptions (from PRD/Production team)

Tracking & Measurement
- UTM params on all links: utm_campaign=youtube_launch, utm_source={channel}, utm_medium={medium}
- Events to instrument (frontend/backend):
  - video_impression (video_id, page, position)
  - video_click (video_id, page, cta_type)
  - youtube_subscribe_click (user_id?, email_opt_in?)
  - video_share (platform)
  - upload_checklist_completed (admin/editor)
- Destination: Segment → Mixpanel/Amplitude. Cohorts: viewers → subscribers
- Dashboard: DAU/Views/Subs by source, CTR, CTR by thumbnail variant

Experiment Ideas
- A/B test CTA copy on hero (Control: "Watch our launch" vs Variant: "See 3 ways [product] saves you time")
- Thumbnail variant test (text-heavy vs minimal)

Owners & Next Steps
- Growth (Jessica): run channel plan, write ad copy, measure experiments
- #ai-backend (Marcus): implement event ingestion + UTM capture, forward to analytics
- #ai-frontend (Kevin): place banners, instrument click events, implement A/B test hooks
- #ai-design (Maya): deliver assets (Task #103)

Measurement window: daily tracking for 90 days. Weekly growth check-ins.

File created by: Jessica (Growth)

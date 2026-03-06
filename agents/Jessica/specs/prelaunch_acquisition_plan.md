Prelaunch Acquisition Plan — Jessica (Growth)

Objective
- Deliver an executable prelaunch acquisition plan with 2 testable channels to build an early user base and validate activation before MVP launch.
- Timeline: experiments live within 2 weeks, evaluation + iterate by end of Q2 (MVP launch target).
- North Star (prelaunch): # activated beta users (activated = completed onboarding key action within 7 days).

Target audience
- Primary: Early-adopter SMB/product teams who need [core value prop].
- ICP signals: product leads, engineering managers, growth PMs at 10–200 employee startups.

Primary KPIs
- Landing page conversion (visit → email capture)
- Activation rate (signup → complete onboarding key action within 7d)
- Cost per activated user (CPA)
- Viral coefficient (for referral channel)

Channel A — Paid Social (Meta + TikTok)
- Hypothesis: Targeted paid social with 2 creative variants will drive high-quality early signups at CPA <$50 and activation rate ≥20%.
- Experiment design:
  - Audience: lookalike of competitors + interest-based (product growth, SaaS, startup)
  - Creatives: 2 variants (product benefit vs onboarding demo). A/B test creatives.
  - Landing page: single CTA ‘Join beta’ → email capture → magic link signup.
  - Tracking: UTM + /api/events tracking for visit, email_capture, signup, activation.
- Sample size & budget:
  - Run for 2 weeks or until 1,000 landing visits per creative (~2k total). Estimated budget $2,000–$5,000 depending on CPC.
- Success criteria:
  - Landing conversion ≥10% (visit→email) AND activation ≥20% OR CPA per activated user <$50.
- Next steps:
  - #ai-design: 2 hero creatives + 15s video by EOD Thu.
  - #ai-frontend: landing + pixel + /api/events for tracking (utm + source) by next Tue. #ai-backend: ensure signup + activation events instrumented.

Channel B — Seeded Referral Beta (Partner seeding + incentivized invites)
- Hypothesis: Seeding 100 high-quality beta users via partner outreach + referral incentives will produce a viral coefficient >0.3 and lower CPA.
- Experiment design:
  - Seed list: 100 invites via partner newsletters / community partners (provide early access code).
  - Referral mechanic: 2 free months credit or swag for 3 successful referrals.
  - Track: invite_sent, invite_accepted, referral_converted, activation.
- Sample size & budget:
  - Seed 100 invites; budget ~$500 for credits/swags.
- Success criteria:
  - At least 20% of seeded users activate within 7 days AND viral coefficient >0.3.
- Next steps:
  - #ai-product: approve partner list and messaging.
  - #ai-support: prepare onboarding checklist for seeded users.
  - #ai-backend: implement referral code tracking endpoint and attribution.

Data & Instrumentation
- Events required: page_view, email_capture, signup, activation, invite_sent, invite_accepted, referral_converted.
- Tagging: UTM params and source to identify channel + creative.
- Analytics: Mixpanel/Amplitude + backup in Postgres for core events. #ai-data: please allocate tracking table.

Timeline & Ownership
- This doc (completed) → output/specs/prelaunch_acquisition_plan.md
- Action owners & deadlines:
  - #ai-design: creatives by Thu EOD
  - #ai-frontend: landing + tracking by next Tue
  - #ai-backend: tracking endpoints + referral by next Tue
  - #ai-product: partner approvals by next Wed
- Evaluation: Run 2-week test windows; report metrics daily. Decision point after 2 weeks: scale or reallocate budget.

Risks & Mitigations
- Slow onboarding activation: add 1:1 onboarding for seeded users; quick feedback loop.
- Tracking gaps: require event contract before launch; block ads until events validated.

Questions / Decisions needed from team
- #ai-product: confirm messaging & top 3 partners to seed by Mon.
- #ai-backend: can you expose simple /api/referral and /api/events by next Tue? If blocked, call it out now.

Summary (Slack-ready)
- Plan uploaded: output/specs/prelaunch_acquisition_plan.md
- Channels: Paid Social (Meta/TikTok) + Seeded Referral Beta
- Immediate asks: #ai-design creatives Thu, #ai-frontend/#ai-backend tracking next Tue, #ai-product partner list by Mon.

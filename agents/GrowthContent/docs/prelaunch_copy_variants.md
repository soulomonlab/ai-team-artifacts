Prelaunch Copy Variants — Landing, Hero, Video & Seeded Outreach

File: output/docs/prelaunch_copy_variants.md

Purpose: High-intent landing & campaign copy for prelaunch acquisition (hero variants, 15s video script, referral messaging, seeded outreach templates, UTM samples).

Decisions
- Tone: confident, helpful, action-first. Target: power users/early adopters who value speed and clear benefit.
- CTA focus: activate within 7 days (complete onboarding key action). Use urgency + clear next step.
- Incentive: credits + limited-edition swag for referrals.
- Attribution: UTM + source param; backup core events to Postgres (as per acquisition plan).

Hero Variant A — "Get Productive Faster"
- Headline: "Ship your best work — 2x faster"
- Subhead: "Smart workflows, zero setup. Get started and complete your first task in under 10 minutes."
- Primary CTA: "Start free — finish onboarding"
- Secondary CTA: "See how it works"
- Microcopy (below CTA): "No credit card. Early access perks for the first 1,000 users."
- UTMs: ?utm_source=paid_social&utm_medium=meta&utm_campaign=prelaunch_heroA

Hero Variant B — "Your Workflow, Reimagined"
- Headline: "Stop wasting time on busywork"
- Subhead: "Automate the tedious parts of your workflow — focus on what moves the needle."
- Primary CTA: "Join the beta — claim credit"
- Secondary CTA: "Get referral code"
- Microcopy: "Invite-only beta: credit + exclusive swag for referrals."
- UTMs: ?utm_source=seeded_referral&utm_medium=email&utm_campaign=prelaunch_heroB

15s Video Script (Social / Landing auto-play, muted)
- Scene 0 (0–2s): Logo card + hook text: "Tired of busywork?"
- Scene 1 (2–7s): Quick product demo showing 1 key automation (visual): "Automate reports in 1 click"
- Scene 2 (7–12s): Benefit + social proof overlay: "Teams save 5+ hours/week — Beta open"
- Scene 3 (12–15s): CTA frame: "Join the beta — get credits & swag" + short URL + referral code prompt
- Visual guidance: fast cuts, clear captions (muted autoplay), on-brand colors

Landing CTAs & Microflows
- Primary funnel: Landing -> Signup -> Guided onboarding checklist (complete key action) -> Activation event within 7d
- Activation copy in onboarding step: "Complete X to unlock $10 credit + referral code"
- Confirmation email subject: "You're in — next: complete onboarding to unlock rewards"

Referral Messaging (web & email)
- Invite email subject: "Your friend invited you to try [Product] — claim your credits"
- Body opening: "Join our early access and get $10 credit when you complete onboarding. Plus, invite friends to earn more."
- CTA: "Claim your spot & get credit"
- Referral card copy on landing: "Share this code: ABC123 — you and your friend get credits"

Seeded Outreach Templates (Short DM + Email)
- DM (Twitter/LinkedIn): "Hey [Name], trying something new — it's fast and saves time. Would love your feedback. Join beta: [short link] — use code: ABC123"
- Seed Email (personalized): "Hi [Name], I’d love your input on a new tool for [role]. Join our beta and get early-access credits + swag. Quick sign-up: [link]"

Tracking hints for Frontend/Analytics
- Primary event: onboarding_completed (fired client-side + POST /api/events) with properties: user_id, utm_source, utm_campaign, referral_code
- Backup: write event to Postgres table events_raw for replay/forwarding to Mixpanel/Amplitude
- Samples UTM patterns: utm_source=[paid_social|seeded_referral|organic], utm_medium=[meta|tiktok|email|dm], utm_campaign=prelaunch_{variant}

Deliverables in this file
- Hero Variant A + B copy
- 15s video script
- Referral & seeded outreach templates
- Tracking copy for frontend

Notes / Next steps
- Design: create two hero creatives + 15s video using the scripts.
- Frontend: wire CTAs, UTM params, and onboarding flow; ensure onboarding_completed event fires.
- Backend: ensure /api/events accepts event payload with utm/referral fields.


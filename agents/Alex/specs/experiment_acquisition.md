# Feature: Acquisition Experiments - CTA Hook & Tracking
**Goal:** Enable three low-budget acquisition experiments by providing frontend CTA hooks, design variants, and Mixpanel-ready tracking so Jessica can run tests and hit her acquisition targets.

**North Star Impact:** Increase new-user signups from acquisition channels (target uplift per experiment defined by Jessica).

**Users:** Marketing (Jessica) running experiments to acquire new users via referral micro-credit, gated demo (SEO), and retargeted onboarding ads with 1-step signup.

**Experiments (provided by Jessica):**
- Referral micro-credit: incentivize invites with small credit applied on signup.
- Gated demo + SEO: require email to access demo content (lead capture) with SEO-driven landing pages.
- Retargeted onboarding ad + 1-step signup: retarget users who saw ads into a simplified signup flow.

**Requirements Summary:**
- Frontend: CTA components/hooks to render experiment-specific copy and A/B variants, fire tracking events on impressions and clicks, and call signup flow.
- Design: Provide CTA copy, visual variants (A/B), placement recommendations for hero, content pages, and modal/inline flows.
- Backend: /api/events ingestion endpoint must accept Mixpanel-ready event payloads (defined below).
- Analytics: Mixpanel events wired for impression, click, and signup conversion with experiment_id and variant labels.

**RICE Score:**
- Reach = 3,000 users/quarter (estimate of users exposed via SEO & ads)
- Impact = 2 (performance)
- Confidence = 70% (estimates from marketing)
- Effort = 1 person-week
RICE = (3000 × 2 × 0.7) / 1 = 4200

**Kano Category:** Performance

**Acceptance Criteria:**
- [ ] Design assets delivered: CTA copy + 2 variants per experiment + placement spec (output/design/...) by Mon EOD
- [ ] Frontend implements CTA hook that:
  - Renders experiment-specific CTA and variant
  - Emits impression event when visible and click event on user action
  - Attaches experiment_id and variant to signup request
  - Integrates with existing signup endpoint (1-step or standard) without regressions
- [ ] Analytics: Events delivered to backend /api/events matching Mixpanel schema and visible in Mixpanel dashboard
- [ ] QA: End-to-end smoke test shows impression → click → signup conversion with correct experiment metadata
- [ ] Performance: Added JS for experiment feature should not increase TTI by >150ms or bundle size by >10KB gzipped

**Tracking (Mixpanel + Backend /api/events) — REQUIRED fields:**
Event names:
- experiment_impression
- experiment_cta_click
- experiment_signup
Common properties (each event):
- experiment_id: string ("referral_credit", "gated_demo", "retarget_onboarding")
- variant: string ("A" | "B" | "control")
- page: string (page or placement id)
- user_id: string|null (if known)
- anonymous_id: string (session or cookie id)
- campaign_source: string|null (utm_source, ad network)
- timestamp: ISO8601
- session_id: string
- referrer: string
- test_group_id: string (optional grouping id)

Example payload (POST /api/events):
{
  "event": "experiment_cta_click",
  "properties": {
    "experiment_id": "referral_credit",
    "variant": "B",
    "page": "landing_v2",
    "user_id": "12345",
    "anonymous_id": "anon_abcdef",
    "campaign_source": "facebook_ads",
    "timestamp": "2026-03-06T12:00:00Z"
  }
}

**Out of Scope:**
- Backend attribution logic & crediting (handled by billing team) — only event ingestion and schema required.
- Full analytics funnels & dashboards (Marketing will build in Mixpanel after events are available).

**Success Metrics (how Jessica measures success):**
- CTR on experiment CTAs (clicks / impressions) by variant
- Conversion rate (signups / clicks) by variant
- New-user acquisition uplift vs baseline per experiment
- Time-to-launch: design+frontend+backend tracking implemented by Mon EOD

**Deadlines & Owners:**
- Alex (Product Owner): spec + tickets created (this file) — DONE
- Maya (Design): CTA copy + 2 variants/experiment + placements — due Mon EOD
- Kevin (Frontend): implement CTA hook, variant rendering, tracking events, integration with signup — due Mon EOD
- Marcus (Backend): ensure /api/events accepts event schema and forwards to Mixpanel — due Mon EOD
- Dana (QA): smoke tests and acceptance — due Mon EOD + 1 day

**Notes / Constraints:**
- Low budget: prefer front-end A/B via client-side variant selection; no heavy backend experimentation platform.
- Keep payloads minimal to avoid extra ingestion costs.

**GitHub Issues:**
- Design ticket created: see issue link in Slack message
- Frontend ticket created: see issue link in Slack message


# Feature: Acquisition Experiments CTA + Tracking

**Goal:** Enable quick frontend CTA hooks and backend event ingestion so Jessica's 3 acquisition experiments can run and be measured in Mixpanel. Launch target: Mon EOD.

**North Star Impact:** Improve top-of-funnel signups and referral conversions; directly supports acquisition experiments target metrics.

**Experiments (Jessica):**
1. Referral micro-credit — CTA invites users to refer friends for micro-credit. (Variant A/B: inline CTA vs modal)
2. Gated demo + SEO — Gated demo that asks for email; CTA placed on SEO landing pages. (Variant A/B: single-field modal vs multi-step flow)
3. Retargeted onboarding ad + 1-step signup — Ad-driven users see a 1-step signup CTA. (Variant A/B: prefill email vs manual)

**Frontend Hook Requirements (to expose to JS and backend):**
- New event: acquisition.cta_click
  - Properties:
    - experiment_id (string) e.g. referral_microcredit
    - variant (string) e.g. A | B
    - cta_location (string) e.g. hero_banner, modal, footer
    - cta_text (string)
    - page_path (string)
    - user_id (nullable string)
    - anonymous_id (string)
    - session_id (string)
    - utm_source / utm_campaign (optional strings)
    - referral_code (optional string)
    - ad_id (optional string)
    - timestamp (ISO8601)

- Secondary event: acquisition.conversion
  - Properties:
    - experiment_id, variant, conversion_type (signup|referral_completed|demo_requested)
    - value (number, optional)
    - user_id, anonymous_id, session_id
    - timestamp

- Implementation notes for frontend:
  - Expose a single JS hook window.trackAcquisitionEvent(eventName, props) that internally calls analytics.track(...) and POSTs to /api/events ingestion endpoint as fallback.
  - Ensure variant is attached from A/B experiment flag (client-side flagging or query param).
  - Fire acquisition.cta_click on CTA interaction; acquisition.conversion when user completes the target action.

**Backend /api/events ingestion:**
- Endpoint: POST /api/events
  - Accepts event_name and properties JSON.
  - Validate required properties (experiment_id, variant, anonymous_id, timestamp).
  - Immediately forward to Mixpanel with server-side token.
  - Store raw events (for debugging) in events_raw table (TTL 30 days).

**Acceptance Criteria:**
- [ ] Design assets (3 CTA copy + 2 variants each + placements) delivered by Maya: Mon, 12:00pm
- [ ] Frontend exposes window.trackAcquisitionEvent and fires acquisition.cta_click with required properties: Kevin implements by Mon, 5:00pm
- [ ] Backend ingestion POST /api/events validates and forwards to Mixpanel: Marcus implements by Mon, 6:00pm
- [ ] Mixpanel dashboards receive events and show experiment_id and variant breakdowns within 1 hour of test: Jessica verifies
- [ ] QA smoke test (Dana): basic flows pass by Mon, 8:00pm

**Tracking / Mixpanel Keys:**
- Distinct ID: user_id || anonymous_id
- Event names: acquisition.cta_click, acquisition.conversion
- Recommended properties for dashboards: experiment_id, variant, cta_location, conversion_type, utm_source, referral_code

**Out of Scope:**
- Full analytics UI or experiment assignment engine (we rely on client flag or query param)
- Long-term event storage beyond 30 days

**Success Metrics:**
- Events tracked for >95% of CTA interactions
- Mixpanel dashboards show variant-specific conversion rate within 1 hour
- Experiment adoption: 3 experiments live and traffic routed

**Deadlines:**
- Design assets: Mon 12:00pm
- Frontend implement: Mon 5:00pm
- Backend ingestion: Mon 6:00pm
- QA smoke: Mon 8:00pm
- Launch target: Mon EOD

**Owner:** Alex (coordination). Contact: #ai-growth (Jessica), #ai-frontend (Kevin), #ai-design (Maya), #ai-backend (Marcus), #ai-qa (Dana)

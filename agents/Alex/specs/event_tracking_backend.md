# Feature: Backend Event Ingestion & UTM Capture
**Goal:** Implement server-side event ingestion endpoints and UTM capture for launch tracking so analytics are reliable and available before frontend rollout.

**North Star Impact:** Ensures all launch events are captured and attributed correctly to measure growth objectives (5k subs, 50k views) and A/B test performance.

**Users:**
- Growth/Marketing (Jessica) — needs reliable events for campaign measurement
- Product/Analytics — needs high-quality event data for Mixpanel/Amplitude

**RICE Score:** Reach=50,000 (expected tracked views/subs) × Impact=2 × Confidence=80% / Effort=2w = 40,000

**Kano Category:** Must-have (for launch analytics and attribution)

**Events to ingest:**
- video_impression
- video_click
- youtube_subscribe_click
- video_share
- upload_checklist_completed

**Requirements:**
- Expose a POST /api/v1/events endpoint that accepts JSON event payloads.
- Capture UTM params (utm_source, utm_medium, utm_campaign, utm_term, utm_content) from query string or event context and persist with the event.
- Validate event schema server-side; reject invalid payloads with 4xx and explanatory errors.
- Persist events in Events table (event_name, user_id/anon_id, timestamp, properties JSON, utm fields, request_id).
- Forward events to Segment (server-side) with retries and DLQ for failures.
- Idempotency: support client-generated event_id to prevent duplicates.
- Rate limit and scale target: handle 200 RPS burst, p95 latency <100ms.
- Privacy: respect opt-out flag (do not forward/persist PII if user.opt_out === true). Ensure PII isn't stored in plain text.

**Acceptance Criteria:**
- [ ] POST /api/v1/events persists valid events and returns 200 with receipt_id.
- [ ] UTM fields are extracted when present in query string and stored with event record.
- [ ] Events are forwarded to Segment; failures retried 3x then placed on DLQ.
- [ ] Duplicate events (same event_id) are deduped within 24 hours.
- [ ] Server-side validation rejects malformed events and returns helpful error codes.
- [ ] End-to-end test: frontend sends video_click with utm params → event present in DB and in Segment within 10s.
- [ ] Documentation for API and sample client instrumentation included in repo docs.

**Out of Scope:**
- Frontend instrumentation (Kevin will handle).
- Analytics dashboards or Amplitude/Mixpanel report configs.

**Success Metrics:**
- 99% of events from launch channels contain UTM fields when present in URL.
- Event ingestion p95 latency <100ms.
- <1% event loss to DLQ after retries.

**GitHub Issue:** TBD (created by Product)

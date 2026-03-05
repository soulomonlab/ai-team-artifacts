# Feature: LinkedIn Uploader (MVP)
**Goal:** Ship a focused MVP to let a single LinkedIn account connect, compose, schedule, and reliably publish posts with delivery logs and basic analytics.

**Users:** Growth marketers, small business owners, internal marketing team (single-tenant)

**Acceptance Criteria:**
- [ ] User can connect one LinkedIn account via OAuth2 (server-side flow) and refresh tokens stored securely.
- [ ] User can compose a post with text + optional image(s) and save as Draft.
- [ ] User can schedule a post for a future time; scheduled posts persist in Postgres.
- [ ] Worker dequeues scheduled posts and publishes to LinkedIn using v2 API with exponential backoff & retry; delivery status recorded.
- [ ] UI shows schedule list (pending, sent, failed) and a composer with templates.
- [ ] Basic analytics available per-post: status, published_at, impressions (if LinkedIn returns), and retry count.
- [ ] Admin logs capture OAuth events, publish attempts, and errors for investigation.
- [ ] Security checklist completed: OAuth best-practices, token encryption, API compliance signed off.

**Success Metrics (MVP):**
- Connect flow success rate >= 95% (during beta)
- Scheduled -> published success rate >= 90% within 72 hours
- Mean time to deliver post <= 5 minutes after scheduled time (95th percentile)
- Beta: 200 testers onboarded; NPS target 40+

**Out of Scope:**
- Multi-tenant org support
- Paid analytics integrations
- Advanced social features (comments, DMs)

**Key decisions:**
- Single-tenant only to reduce scope.
- Use Postgres for canonical data, Redis (or RabbitMQ) for scheduling queue, workers for delivery.
- OAuth2 server-side flow; store refresh tokens encrypted in DB.
- Design queue + backoff to respect LinkedIn rate limits.

**MVP Ticket List (GitHub issues):**
1. MVP Epic: LinkedIn Uploader - track all sub-tasks (#TBD)
2. OAuth2: LinkedIn connect + token storage (backend)
3. Backend API: Create/Update/Delete posts, schedule endpoint
4. Scheduler + Workers: queue, delivery logic, retry/backoff, rate-limiting
5. UI Composer: composer + templates (design + frontend)
6. Schedule List UI: list, filters, status (pending/sent/failed)
7. Analytics & Admin Logs: basic per-post analytics + admin logs
8. DevOps: infra plan (K8s, queue, secrets), cost estimate
9. Security: OAuth & API compliance checklist + risk items
10. QA & Support: support playbook, failure-handling guide
11. Growth & Beta: beta signup copy + tester list

**Blockers / Immediate Risks:**
- Need LinkedIn developer access and app credentials (API access) — if not available, cannot validate publish flow.
- Legal/API compliance review may require changes.

**Branch:** feature/marketing/linkedin-uploader (created)

**Spec file:** output/specs/linkedin_uploader_mvp.md


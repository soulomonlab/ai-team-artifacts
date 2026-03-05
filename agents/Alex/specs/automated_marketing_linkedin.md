# Feature: Automated Marketing + LinkedIn Post Uploader
**Goal:** Enable users to create marketing campaigns, schedule LinkedIn posts, and automate multi-channel delivery with analytics.

**Users:** Marketing teams, growth managers, small-business owners.

**Acceptance Criteria:**
- [ ] User can connect their LinkedIn account via OAuth and grant posting permissions.
- [ ] User can create a campaign with one or more LinkedIn posts (text, image, link), save as draft, and schedule publish time.
- [ ] System queues scheduled posts and reliably posts to LinkedIn at the scheduled time; retries on transient failures with exponential backoff.
- [ ] User can upload or select post templates and reuse them across campaigns.
- [ ] Dashboard shows per-post status (scheduled, posted, failed), basic metrics (impressions, clicks) where LinkedIn provides data.
- [ ] System enforces LinkedIn API rate limits and surfaces errors to the user.
- [ ] Security: OAuth tokens stored encrypted; only authorized users can manage their organization's campaigns.
- [ ] Admins can revoke connections and view integration logs.

**Edge cases:**
- Token refresh failures → surface error and notify user to reconnect.
- LinkedIn API downtime → mark post failed, retry policy, and provide manual retry option.
- Duplicate scheduling attempts → idempotency keys to prevent double-posting.

**Out of Scope:**
- Posting to other social networks (future work).
- Advanced social analytics (beyond basic metrics returned by LinkedIn).

**Key Decisions (initial):**
- Use LinkedIn REST API with OAuth2 (server-side flow). 
- Backend service responsible for scheduling/queueing (separate worker queue). 
- Store tokens encrypted at rest; use scoped secrets for per-org tokens.
- Use idempotency keys for post creation to prevent duplicates.

**GitHub Issue:** #TBD

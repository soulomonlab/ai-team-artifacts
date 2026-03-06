# Feature: Funny Meme App (v1)
**Goal:** Enable users to create, edit, share, and discover short static-image memes with a delightful, low-friction UX.
**North Star Impact:** Increase daily active users (DAU) and time-on-site by offering a viral, shareable content loop.
**Users:**
- Casual social users who want to create/share jokes quickly.
- Creators who want lightweight editing and viral distribution.

**RICE Score:** Reach=30,000 × Impact=2 × Confidence=60% / Effort=6w = 6,000
**Kano Category:** Performance (core social engagement feature)

**Acceptance Criteria:**
- [ ] User can upload an image (jpg/png <= 10MB) and add up to 3 text overlays with font/size/color.
- [ ] User can position and drag text overlays, preview, and save a meme.
- [ ] User can publish meme to a public feed and copy a shareable link.
- [ ] Users can like and comment on public memes. Feed is paginated and supports infinite scroll.
- [ ] Backend stores images in object storage (S3), metadata in relational DB, and serves thumbnails.
- [ ] Anti-abuse: basic profanity filter (server-side) and user report flow.
- [ ] Performance: feed API 95th percentile latency <300ms; system scales to 5k concurrent uploads/day initially.

**Out of Scope:**
- Video/GIF meme editor, advanced moderation (ML-based), multi-user collaborative editing.

**Success Metrics:**
- DAU from meme feed >= 10k within Q1 post-launch.
- Share rate: >=15% of created memes are shared externally.
- Median time from upload→publish < 30s.

**Implementation Notes / Key Decisions:**
- Storage: S3 for images + CloudFront for CDN.
- DB: Postgres for metadata (rich querying + JSON fields for extensibility).
- Auth: JWT with optional social login in v1.
- Image processing: serverless worker to generate thumbnails and overlay rendering.
- Moderation: start with server-side profanity filter + user reports; escalate to ML later.

**GitHub Issue:** TBD (will create)

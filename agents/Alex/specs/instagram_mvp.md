# Feature: Instagram-like Mobile & Web App (MVP)
**Goal:** Build an Instagram-style app enabling users to share photos, follow others, and engage with a scalable backend.

**North Star Impact:** Increase user engagement (DAU/MAU) by providing an intuitive feed + easy media sharing experience.

**Users:**
- Casual users: post photos, browse feed, like/comment (onboarding -> posting -> social engagement)
- Content creators: publish and grow followers
- Power users: search hashtags, follow trends

**RICE Score:** Reach=10,000 users/q × Impact=2 × Confidence=60% / Effort=8w = 1500

**Kano Category:** Performance

**Acceptance Criteria:**
- [ ] Users can sign up, login (email/password, OAuth optional), and maintain sessions (JWT + refresh tokens).
- [ ] Users can upload photos (single + multi), which are stored in S3 and served via CDN.
- [ ] Uploaded images are processed into thumbnails + web sizes asynchronously; original retained.
- [ ] Users can see a chronological + relevance-ranked feed of posts from people they follow.
- [ ] Users can like and comment on posts; likes and comments appear in real time (eventual consistency ok).
- [ ] Users can follow/unfollow other users; social graph stored in DB with efficient fanout queries.
- [ ] Basic hashtag search for posts.
- [ ] System handles 10k DAU with p95 API latency <200ms for feed endpoints under target load; error rate <1%.
- [ ] Security: rate limits, input validation, auth checks for media access.

**Out of Scope (MVP):**
- Reels/short video, ads, advanced discovery algorithms, in-app purchases, analytics dashboard for creators.

**Success Metrics:**
- MAU in first quarter after launch >= 10k
- Day-1 retention >= 35%
- Avg session length >= 4 minutes
- Post upload success rate >= 99.5%

**Key Decisions (initial):**
- Media storage: S3 (single source of truth) + CDN (CloudFront) for delivery — reversible and cost-effective.
- Database: PostgreSQL for core relational data (users, posts, follows); Redis for caching and rate-limiting.
- Processing: asynchronous image processing via serverless jobs (Lambda / background workers).
- API: RESTful endpoints first (fast to iterate); consider GraphQL later if client payload needs increase.
- Auth: JWT access tokens (short-lived) + refresh tokens; passwords stored with bcrypt.

**GitHub Issue:** TBD (created by Product Owner)


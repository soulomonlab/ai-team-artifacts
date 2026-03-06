# Feature: Recipe App (MVP)
**Goal:** Let users discover, save, and share recipes with a fast, beautiful UX and a scalable backend.
**North Star Impact:** Increase weekly active users (WAU) and time-on-site by providing sticky content and social-shareable recipes.
**Users:** Home cooks (primary), food bloggers (secondary), casual browsers

**RICE Score:**
- Reach = 25,000 users / quarter
- Impact = 2 (meaningful improvement in engagement)
- Confidence = 80%
- Effort = 6 person-weeks
RICE = (25,000 × 2 × 0.8) / 6 ≈ 6,666

**Kano Category:** Performance (core product feature)

**Acceptance Criteria:**
- [ ] Users can view a feed of recipes with images, tags, cook time, and ratings
- [ ] Users can search recipes by name, ingredient, or tag with results < 300ms
- [ ] Authenticated users can save recipes to their profile and create collections
- [ ] Authenticated users can create and edit recipes (title, ingredients, steps, images, tags)
- [ ] Users can share a recipe via URL and social share metadata (Open Graph)
- [ ] Rate-limiting and pagination are in place for feeds and search
- [ ] Backend scales to 10k concurrent reads with response p95 < 500ms

**Out of Scope:**
- Advanced personalization / recommendations (ML)
- Mobile-native apps (initially web-first)
- Payments and premium features

**Success Metrics:**
- 60% feature adoption (saved recipe at least once) among new signups in 30 days
- WAU +20% in first quarter after launch
- p95 API latency < 500ms, error rate < 1%

**Initial API Surface (MVP):**
- GET /recipes (feed, filters, pagination)
- GET /recipes/:id
- POST /recipes (auth)
- PUT /recipes/:id (auth, owner)
- POST /users/:id/saved (save/unsave)
- GET /users/:id/collections

**Tech Decisions (initial):**
- DB: Postgres (JSONB for flexible ingredients & tags)
- Search: Postgres full-text + indexes; Redis for caching hot reads
- Hosting: Kubernetes on cloud provider (Taylor to confirm infra)

**GitHub Issue:** TBD

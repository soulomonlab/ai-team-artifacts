# Feature: Recipe App (MVP)
**Goal:** Enable users to discover, save, and follow step-by-step recipes with an intuitive mobile-first experience and scalable backend.

**North Star Impact:** Increase DAU and time-in-app by providing sticky recipe discovery and saving flows.

**Users:**
- Home cooks (primary): discover recipes, filter by diet/allergies, save favorites, follow steps
- Casual browsers: search for quick recipes, view ingredients and nutrition

**RICE Score:**
- Reach = 10,000 users / quarter
- Impact = 2 (Performance)
- Confidence = 70%
- Effort = 6 person-weeks
- RICE = (10,000 × 2 × 0.7) / 6 ≈ 2,333

**Kano Category:** Performance

**Acceptance Criteria:**
- [ ] Users can browse recipe feed with images, cook time, and tags
- [ ] Users can search and filter by keyword, ingredient, diet, cook time
- [ ] Users can view full recipe details: ingredients, steps, nutrition, servings
- [ ] Users can save/unsave recipes to personal favorites
- [ ] Users can create and edit their own recipes (auth required)
- [ ] API responses < 300ms p95 under load of 500 RPS
- [ ] Basic input validation + XSS protection for user-submitted content

**Out of Scope (MVP):**
- Social features (comments, follows) beyond favorites
- Video step-by-step walkthroughs
- Advanced personalization / recommendation ML

**Success Metrics:**
- Adoption: 30% of new users save ≥1 recipe within 7 days
- Engagement: DAU for recipe flows increases by 20% in 90 days
- Performance: API error rate < 1% and p95 latency < 300ms

**Key Decisions (initial):**
- Backend: Postgres with JSONB for recipe steps/ingredients to balance relational queries + flexibility
- API: REST v1 for MVP; design OpenAPI after initial endpoints
- Auth: JWT for mobile/web sessions

**Minimum Viable API Endpoints (v1):**
- GET /v1/recipes — list + filters
- GET /v1/recipes/{id} — recipe details
- POST /v1/recipes — create (auth)
- PUT /v1/recipes/{id} — update (auth/ownership)
- POST /v1/recipes/{id}/favorite — toggle favorite (auth)
- GET /v1/users/{id}/favorites — list user favorites

**Next Steps:**
1. Tech lead: repo + initial infra scaffolding
2. Design: create mobile + web wireframes (browse, recipe detail, create)
3. Backend: implement DB schema + REST endpoints + tests
4. Frontend: implement feed, detail, save flows

**Spec file:** output/specs/recipe_app.md

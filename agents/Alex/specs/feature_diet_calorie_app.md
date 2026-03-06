# Feature: Diet Calorie App (v1)
**Goal:** Provide a simple, accurate way for users to track daily calories and macros with minimal friction.

**North Star Impact:** Increase daily active retention for health-focused users; expected to improve user satisfaction for diet-tracking flows.

**Users:**
- Primary: Health-conscious consumers who want to track calories/macros (logging meals, quick lookup).
- Secondary: Dietitians who want a quick lightweight tracking tool for clients.

**RICE Score:** Reach=20,000 × Impact=2 × Confidence=80% / Effort=6w = 5,333

**Kano Category:** Performance

**Key decisions:**
- Start with mobile-first UX, web responsive. Barcode scanning is optional for v1 (MVP: manual search + recent foods + favorites).
- Backend: PostgreSQL for relational data + fast food lookup (JSONB for food metadata). REST API v1 (later GraphQL if needed).
- Use existing food database (USDA or open food DB) as seed data to avoid building a dataset from scratch.
- Authentication: OAuth + Email; sessions via JWT for mobile/web parity.

**Acceptance Criteria:**
- [ ] User signup/login (email + OAuth).
- [ ] User can search foods, view calories/macros per serving.
- [ ] User can log meals (meal name, items, servings, timestamp).
- [ ] Daily summary page shows total calories + macro breakdown.
- [ ] User can set daily calorie target and track progress.
- [ ] Backend endpoints documented (API v1) and pass basic integration tests.
- [ ] System supports 10k daily active users with <200ms median API latency under normal load.

**Out of Scope (v1):**
- Barcode scanner (defer to v1.1)
- Social sharing / challenges
- Advanced diet plans or coaching

**Success Metrics:**
- Adoption: 60% of onboarding users log at least one meal within 7 days.
- Retention: 30-day retention >= 25% (baseline target)
- Latency: 95th percentile API < 500ms

**Implementation milestones:**
1. Spec & product issue (this doc)
2. API design + data model (backend)
3. Mobile/web UI designs (Maya)
4. Backend implementation (Marcus)
5. Frontend implementation (Kevin)
6. QA + beta

**GitHub Issue:** TBD

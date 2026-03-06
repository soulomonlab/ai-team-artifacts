# Feature: Diet Calorie App (MVP)
**Goal:** Provide users an intuitive mobile/web app to track daily calories, meals, and weight goals with scalable backend support.

**North Star Impact:** Increase daily active users and retention by helping users meet calorie goals; target +15% 30-day retention for diet users.

**Users:**
- Persona: Busy professional who wants simple calorie tracking to lose/maintain weight.
- Use case: Quickly log meals, set calorie goal, view daily/weekly summaries, and track progress.

**RICE Score:** Reach=5,000 users/quarter × Impact=2 × Confidence=80% / Effort=4w = 2,000
**Kano Category:** Performance (core product value)

**Acceptance Criteria:**
- [ ] User can create account and set daily calorie goal (kcal).
- [ ] User can add meals with name, calories, timestamp, and optional photo.
- [ ] System shows daily total, remaining calories, and 7-day trend chart.
- [ ] User can edit/delete meals; changes reflected in real-time on dashboard.
- [ ] API responds <200ms p95 for read endpoints; write endpoints <300ms p95 under 100 RPS.
- [ ] Data stored securely; personal data encrypted at rest.
- [ ] Basic auth (JWT) and rate limiting implemented; growth-ready pagination for meal history.

**Out of Scope:**
- Food database search / barcode scanning (v2).
- Advanced nutrition breakdown (macros) beyond calories (v2).

**Success Metrics:**
- Adoption: 60% of signups log at least one meal in first week.
- Retention: 15% uplift in 30-day retention vs baseline.
- Reliability: API error rate <1% in first month; latency targets met.

**Initial Tech Decisions:**
- Backend: REST API (JSON) using Postgres for meals + Redis for caching; chosen for relational queries and scalability.
- Auth: JWT access tokens with refresh tokens.
- Storage: Images stored in object storage (S3-compatible) with CDN.

**Milestones (MVP):**
1. API + DB schema (Marcus)
2. Core frontend screens + components (Kevin)
3. Design system & UX flows (Maya)
4. QA test plan (Dana)

**GitHub Issue:** (created by product owner)

# Feature: Quick-win MVP — Auth + Profile + Homepage stub
**Goal:** Deliver a minimal end-to-end experience so we can test core UX and backend scalability assumptions quickly.
**North Star Impact:** Faster user activation + measurable engagement from first-run users; enables iteration on onboarding flow.
**Users:** New users evaluating the product (persona: early adopters wanting quick setup and immediate value).
**RICE Score:** Reach=10000 × Impact=2 × Confidence=80% / Effort=4w = 4000
**Kano Category:** Performance (core onboarding) / Must-have for launch

**Scope (in):**
- Backend: JWT-based auth (signup, login, refresh), user profile CRUD, healthcheck, rate-limited endpoints
- Frontend: Simple responsive homepage, signup/login flows, profile page (stub)
- Design: Minimal brand styling + component kit for forms
- QA: End-to-end tests for auth flows, basic load test for auth endpoints

**Acceptance Criteria:**
- [ ] POST /api/v1/signup creates user, returns JWT access + refresh
- [ ] POST /api/v1/login returns JWTs for valid credentials
- [ ] GET /api/v1/me returns user profile when authenticated
- [ ] PUT /api/v1/me updates profile fields (name, avatar_url)
- [ ] Frontend: Signup/login/profile pages implemented and wired to backend
- [ ] Healthcheck endpoint /api/v1/health returns 200 with DB and Redis status
- [ ] Load test: Auth endpoint sustains 200 RPS with p95 latency < 200ms in dev staging
- [ ] Basic E2E tests covering signup -> login -> profile update

**Out of Scope:**
- Social login (OAuth), email verification, payments, advanced profile features

**Success Metrics:**
- 75% of test users complete signup within 90s
- Auth p95 latency < 200ms under staging load
- Activation rate (signup -> first profile update) > 60% in pilot cohort

**Implementation Notes / Decisions:**
- Use JWTs (short-lived access + refresh) for simplicity and scalability
- Postgres for user store; Redis for refresh token blacklist + rate limiting
- API contract: JSON RESTful endpoints under /api/v1

**Next Steps / GitHub:**
- Create repo branch: feature/quick-win-mvp
- Linked tasks created for backend, frontend, design, QA

**Files:** output/specs/quick-win_mvp.md

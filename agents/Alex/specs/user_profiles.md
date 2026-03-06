# Feature: User Profiles API v1
**Goal:** Provide a scalable, secure CRUD + list API for user profiles with JWT auth, RBAC, idempotency, and rate-limiting.

**North Star Impact:** Improves user onboarding and personalization (directly affects user satisfaction and retention).

**Users:**
- Primary: Registered users (view/edit their profile)
- Secondary: Admins (manage user profiles)
- API consumers: Mobile/web frontends

**RICE Score:** Reach=15000 × Impact=3 × Confidence=80% / Effort=3w = 12000

**Kano Category:** Must-have

**Decisions (key):**
- DB: Postgres (primary). Use UUID PKs, indexed email and updated_at.
- API base: /api/v1/users. Pagination: ?page & ?size (default page=1,size=20,max=100).
- Auth: Bearer JWT for all endpoints. JWT includes sub=user_id, roles claim.
- RBAC: Roles={admin, user}. Admin can CRUD any profile; user can read/update own profile; delete restricted to admin.
- Idempotency: Mutating ops (POST/PUT/DELETE) must accept Idempotency-Key header and persist keys for 24h to make ops idempotent.
- Rate limiting: Per-user default 100 requests/min with 429 responses. Configurable per-env. Use token-bucket (Redis-backed) for distributed rate-limiting.
- Caching: Optional Redis cache for list endpoint (ttl 30s) if list latency exceeds targets.
- Observability: OpenTelemetry traces. Capture spans for requests >50ms. Exporter configured in infra.
- Perf targets: p95 <100ms, p99 <200ms for API layer.

**API Endpoints:**
- GET /api/v1/users?page=&size=  — list users (admin) or own profile (user limited)
- GET /api/v1/users/{id} — get profile (admin or owner)
- POST /api/v1/users — create user profile (idempotent)
- PUT /api/v1/users/{id} — update profile (idempotent)
- DELETE /api/v1/users/{id} — delete profile (admin only, idempotent)

**Acceptance Criteria:**
- [ ] CRUD endpoints implemented and documented under /api/v1/users
- [ ] List endpoint supports pagination ?page & ?size and returns total count + pages
- [ ] JWT Bearer auth enforced; unauthorized returns 401
- [ ] RBAC enforced per-role rules above
- [ ] Idempotency-Key implemented for POST/PUT/DELETE with dedup window 24h
- [ ] Rate limiting enforced (per-user) and configurable via env
- [ ] DB migrations for user_profiles table (uuid id, email unique, name, bio, metadata jsonb, created_at, updated_at)
- [ ] Observability: OpenTelemetry spans emitted; capture traces >50ms
- [ ] Performance: p95 <100ms; p99 <200ms under normal load tests
- [ ] Integration tests (API + auth + RBAC) and unit tests for service layer

**Out of Scope:**
- File uploads for avatars (handled later by a dedicated media service)
- Full-text search/filtering (paging + basic filters only)

**Success Metrics:**
- API latency: p95 <100ms, p99 <200ms
- Error rate <1% for profile endpoints
- 90% of user profile edits succeed without conflict (idempotency working)
- Adoption: 60% of active users have a profile completed within 14 days

**GitHub Issue:** #TBD

# User Profiles API v1 - Spec

## Summary
CRUD + list (pagination) for user profiles. Auth: Bearer JWT. RBAC: admin/user. Idempotent mutating ops. Rate-limited endpoints.

Base path: /api/v1/users
Pagination: ?page=<int>&?size=<int> (defaults page=1,size=20, max size=100)

Perf targets: p95 < 100ms, p99 < 200ms.
Cache: Redis for list endpoint (stale-while-revalidate) if load warrants.
Observability: OpenTelemetry traces; sample endpoints >50ms.

## Key Decisions
- DB: Postgres (UUID PKs).
- Auth: Bearer JWT with `sub`, `roles` claims. Service validates JWT. Role-based checks enforced in API layer.
- RBAC roles: `admin`, `user`. Users can CRUD only their own profile; admin can CRUD any.
- Idempotency: Mutating requests (POST/PUT/DELETE) must accept `Idempotency-Key` header. Server stores idempotency result (short TTL) to ensure safe retries.
- Rate limiting: 100 req/min per user by default; stricter for unauthenticated endpoints. Use Redis-backed token bucket.
- Observability: Add tracing to all endpoints; emit spans when handler runtime >50ms. Log structured events for CRUD ops.

## Data Model (Postgres)
Table: users
- id: UUID PRIMARY KEY
- email: text UNIQUE NOT NULL
- display_name: text
- bio: text
- avatar_url: text
- metadata: jsonb DEFAULT '{}'
- role: text CHECK (role IN ('user','admin')) DEFAULT 'user'
- created_at: timestamptz
- updated_at: timestamptz
- last_login: timestamptz

Indexes:
- unique(email)
- idx_users_role (role)
- idx_users_created_at (created_at DESC)

Considerations: keep PII minimal; do not store passwords here (auth service handles credentials).

## API Endpoints
All endpoints require Authorization: Bearer <JWT> unless noted.

1) List users
GET /api/v1/users?page=&size=&q=
- Query params: page, size, q (optional search by email/display_name)
- Response: { items: [User], page, size, total }
- Caching: cache pages for 30s; use Redis with cache-key based on query + page + size; invalidate on profile updates.

2) Get user
GET /api/v1/users/{id}
- Authorization: user can get own id or admin
- Response: User object

3) Create user (idempotent)
POST /api/v1/users
- Body: { email, display_name, bio?, avatar_url?, metadata? }
- Headers: Idempotency-Key
- Admins can create users; or allow service-to-service flows.
- Response: 201 Created + Location header

4) Update user (idempotent)
PUT /api/v1/users/{id}
- Body: partial or full update (upsert semantics allowed)
- Headers: Idempotency-Key
- Authorization: self or admin
- Response: 200 OK

5) Delete user (idempotent)
DELETE /api/v1/users/{id}
- Headers: Idempotency-Key
- Authorization: admin (or support role)
- Soft-delete recommended: set deleted_at column and anonymize PII

Idempotency semantics: server stores mapping (Idempotency-Key -> response/status) for 24h. On duplicate key, return previous response.

## Security
- Validate JWT signature and expiry. Use JWKS or shared secret per environment.
- Enforce least privilege. Admin-only endpoints require role check.
- Rate-limit per user (JWT.sub). For unauthenticated fallback to IP-based limit.
- Input validation & size limits for fields (display_name <= 64 chars, bio <= 1024 chars).
- No sensitive PII in logs.

## Observability & Metrics
- HTTP metrics: requests_total, requests_latency_seconds{quantile}
- Auth failures, idempotency hits/misses, cache hits/misses
- Traces via OpenTelemetry; sample traces for requests >50ms.

## Errors
Use standard API error envelope: { code, message, details? }
HTTP status codes: 200,201,400,401,403,404,409 (idempotency conflict), 429,500

## Implementation notes for Backend
- Use FastAPI, Pydantic models, async DB access via asyncpg/SQLAlchemy Core.
- Use Redis for cache + rate-limiting + idempotency storage.
- Add middleware for JWT auth, RBAC enforcement, rate-limiting, idempotency handling.
- DB migration via Alembic. Add users table migration.

## Acceptance Criteria
- Endpoints implemented on branch feature/user-profiles.
- Automated tests covering auth, RBAC, idempotency, rate-limiting, pagination.
- Docs: this spec added to output/specs/user_profiles.md
- Performance: benchmarks showing p95/p99 targets or plan for caching.


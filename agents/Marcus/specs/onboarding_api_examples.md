# Onboarding API - examples & auth decision

Location: output/specs/onboarding_api_examples.md

Purpose: Concrete request/response examples for frontend mocks (signup, profile, initial onboarding tasks) + auth approach decision.

Auth decision (backend):
- Hybrid JWT approach (recommended):
  - Short-lived Access Token (JWT), expires in 15 minutes. Sent in Authorization: Bearer <access_token> header.
  - Refresh Token stored in an HttpOnly, Secure, SameSite=Strict cookie and rotated on refresh. Refresh endpoint: POST /api/v1/auth/refresh
  - Logout/revoke endpoint: POST /api/v1/auth/logout (clears cookie + revokes refresh token).
  - Rationale: stateless access, low latency for APIs; refresh cookie mitigates XSS risk vs storing refresh token in localStorage.
  - #ai-security (Isabella) please review.

Notes for frontend mocks:
- For local/dev mock convenience we can return a refresh_token in the response body when ?dev=true, but prod will only set cookie.
- All endpoints are under /api/v1 and require Authorization where noted.

Standard error format (JSON):
{ "error": { "code": "<machine_code>", "message": "Human-friendly message", "details": { /* optional */ } } }

API Summary
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST   | /api/v1/auth/signup | Create account + issue tokens | none |
| POST   | /api/v1/auth/login | Exchange creds for tokens | none |
| POST   | /api/v1/auth/refresh | Rotate refresh token, return access token | refresh cookie |
| POST   | /api/v1/auth/logout | Revoke refresh token, clear cookie | refresh cookie or Authorization |
| GET    | /api/v1/users/me | Get current user profile | Bearer |
| GET    | /api/v1/users/me/onboarding_tasks | Get onboarding tasks | Bearer |


1) Signup
Request
POST /api/v1/auth/signup
Headers: Content-Type: application/json
Body:
{
  "email": "kevin@example.com",
  "password": "Str0ngP@ss!",
  "name": "Kevin Frontend"
}

Success (201)
Response JSON:
{
  "user": {
    "id": "7f9d6c3a-1a2b-4c6d-9e8f-0123456789ab",
    "email": "kevin@example.com",
    "name": "Kevin Frontend",
    "onboarded": false,
    "created_at": "2026-03-04T12:00:00Z"
  },
  "access_token": "<jwt-access-token>",
  "token_type": "bearer",
  "expires_in": 900
}

Notes: server will also SET-COOKIE: refresh_token=<token>; HttpOnly; Secure; SameSite=Strict; Path=/api/v1/auth/refresh; Max-Age=604800

Errors
400 Bad Request ->
{
  "error": { "code": "invalid_input", "message": "Password too weak" }
}
409 Conflict -> email already exists


2) Login
Request
POST /api/v1/auth/login
Body:
{
  "email": "kevin@example.com",
  "password": "Str0ngP@ss!"
}

Success (200)
{
  "user": { "id": "...", "email": "kevin@example.com", "name": "Kevin Frontend", "onboarded": false },
  "access_token": "<jwt-access-token>",
  "token_type": "bearer",
  "expires_in": 900
}
(Set-Cookie: refresh_token=... as above)


3) Refresh
Request
POST /api/v1/auth/refresh
Headers: Cookie: refresh_token=<token>

Success (200)
{
  "access_token": "<new-access-token>",
  "token_type": "bearer",
  "expires_in": 900
}

Errors: 401 if refresh invalid/expired -> client should redirect to login


4) Get profile
Request
GET /api/v1/users/me
Headers: Authorization: Bearer <access_token>

Success (200)
{
  "id": "7f9d6c3a-...",
  "email": "kevin@example.com",
  "name": "Kevin Frontend",
  "avatar_url": null,
  "onboarding_state": {
    "current_step": 1,
    "completed": false
  },
  "preferences": {
    "timezone": "UTC",
    "language": "en"
  }
}

401 Unauthorized -> standard error JSON


5) Initial onboarding tasks
Request
GET /api/v1/users/me/onboarding_tasks?page=1&size=20
Headers: Authorization: Bearer <access_token>

Success (200)
{
  "tasks": [
    {
      "id": "task-1",
      "title": "Complete profile",
      "description": "Add a photo and short bio",
      "status": "pending", // pending | completed | skipped
      "order": 1
    },
    {
      "id": "task-2",
      "title": "Connect calendar",
      "description": "Link your Google Calendar to sync events",
      "status": "pending",
      "order": 2
    }
  ],
  "meta": { "total": 2, "page": 1, "size": 20 }
}

PATCH /api/v1/users/me/onboarding_tasks/:id
Body: { "status": "completed" }
Response: 200 -> updated task object


Developer notes / SLAs
- p99 < 200ms for profile and onboarding tasks endpoints; these are cachedable per-user in Redis for 5 minutes.
- DB: users table + onboarding_tasks table (simple schema). We'll add proper indexes on user_id.

Next actions / handoffs
- #ai-tech-lead (Taylor) — confirm repo name & CI visibility so Kevin can create feature/frontend/init branch.
- #ai-security (Isabella) — please review JWT + refresh-cookie approach.
- #ai-design (Maya) — upload mid-fi onboarding to output/design/onboarding_sketches.pdf.
- #ai-qa (Dana) — use these examples to start acceptance tests for onboarding flows.
- #ai-frontend (Kevin) — use this file for mocks. If you want a mock server I can spin up a tiny FastAPI dev branch.

File created by Marcus (backend).
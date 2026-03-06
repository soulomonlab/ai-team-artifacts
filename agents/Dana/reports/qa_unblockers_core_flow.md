QA Unblockers & Test Plan — Core Flow (Dana)

File: output/reports/qa_unblockers_core_flow.md

Summary
- Purpose: List backend spec details QA needs before starting test design and automation.
- Use this to confirm decisions in the API spec (OpenAPI) Marcus will publish and to align frontend inputs from Kevin/Maya.

Required API-level confirmations (blockers until answered)
1) Auth
   - Preferred: Bearer JWT for access tokens + refresh token flow.
   - Need exact values: access token expiry (e.g., 15m), refresh expiry (e.g., 7d), refresh rotation strategy, token revocation mechanism, scopes/claims mapping.
   - Acceptance check: Auth endpoints documented with request/response examples and error cases (401, 403).

2) Pagination
   - Preference: cursor pagination for scalability. If offset chosen, include total_count.
   - Need details: cursor token format, page size limits (min/max/default), stable sorting fields.
   - Acceptance: OpenAPI includes examples, and list endpoints return next_cursor and has_more OR total_count if offset.

3) Core resource item shape
   - Fields required: id (UUID), title (string, max length), status (enum), created_at/updated_at (ISO8601), optional metadata JSON.
   - Validation rules for each field.
   - Acceptance: schema definitions in OpenAPI and example payloads.

4) Error format
   - Preferred structure: { code: string, message: string, details?: object } or RFC7807 problem+json.
   - Include validation error shape for 4xx with field-level errors.
   - Acceptance: documented global error schema.

5) Realtime / WebSocket
   - Confirm whether realtime is needed for core flow. If yes, provide events, auth for WS, at-least-once vs exactly-once expectations.

6) Rate limits & auth scopes
   - Provide rate limit policy per endpoint (requests/minute) and auth scopes for each action.

7) Side effects & consistency
   - Transactional guarantees for mutating endpoints (idempotency keys? eventual consistency?).

QA Test Strategy (high level)
- Coverage target: >90% test coverage for backend contract-related tests.
- Automation: automate acceptance, integration, and security tests. Manual exploratory for complex flows.
- Types of tests to be produced once spec+PR available:
  1) Unit tests: validation logic, boundary values (title length, status values)
  2) Integration tests: full API contract using OpenAPI examples, DB state checks
  3) End-to-end acceptance tests (mocked frontend) covering happy path + error flows
  4) Security tests: auth bypass, stale/rotated refresh token, JWT tampering, injection
  5) Load/Performance smoke: verify pagination stability under concurrent reads

Test design notes (to include in test files)
- Equivalence classes: valid vs invalid tokens, valid vs invalid payloads, empty lists vs large lists (>page size), single-item updates vs concurrent updates.
- Boundary analysis: title length (0,1,max,max+1), page size (1, default, max+1), timestamp formats.
- Decision table example: Create item -> valid token & valid payload = 201; invalid token = 401; missing required field = 400 + field errors.

Risk areas
- Token refresh rotation bugs (stolen refresh tokens)
- Pagination tokens invalidation leading to inconsistent results
- Missing validation causing DB errors (SQL injection, large payloads)
- Race conditions on concurrent updates

Deliverables I will produce once OpenAPI + frontend mocks/PRs exist
- output/tests/test_core_api_unit.py (unit tests)
- output/tests/test_core_api_integration.py (integration + OpenAPI contract tests)
- output/reports/qa_test_report_core_flow.md (run results + coverage)

Immediate asks / next steps (for Marcus / Alex)
- @Marcus (#ai-backend): please confirm the seven items above in the API spec. If you prefer defaults, state them explicitly in OpenAPI (token TTLs, pagination type, error schema).
- @Alex (#ai-product): if any business rules affect validation/status values, list them so QA can encode in tests.

Timing
- Once OpenAPI + design files are published: I'll create test stubs within 24 hours and run initial suite. Expect iterative PR reviews.

QA gate
- I'll block release if coverage <90% for contract tests or if any P1 security/auth bug found.


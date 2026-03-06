# Feature: MVP Scope & Acceptance Criteria (Q2)
**Goal:** Deliver a usable MVP with excellent UX, scalable backend, and high code quality within ~8 weeks.

**North Star Impact:** Launch a functional product that drives 60% feature adoption among trial users and meets p95 latency <200ms.

**Users:**
- Primary: Early adopters (power users) who need to create, share, and find content quickly.
- Secondary: Team admins managing users and access.

**Top 5 Features (Must-have):**
1. Authentication & Account Management
   - Email/password signup, OAuth (Google) optional for MVP.
   - Email verification, password reset.
2. Core Item CRUD (Create / Read / Update / Delete)
   - Users can create, edit, delete core content ("items" / "projects").
   - Versioning or simple change history.
3. Sharing & Permissions
   - Share items with users or teams (read / write roles).
   - Invite flow and access control checks.
4. Search & Filter
   - Full-text search across items, basic filters (owner, date, tag).
   - Results ranked by relevance, pagination.
5. Activity Feed & Notifications
   - In-app feed for item activity (create/update/share).
   - Optional email notifications for invites and important events.

**RICE Score (overall MVP):**
- Reach = 10,000 users/quarter
- Impact = 2 (substantial) 
- Confidence = 75% 
- Effort = 6 person-weeks
- RICE = (10,000 × 2 × 0.75) / 6 ≈ 2,500

**Kano Category:** Must-have (minimum viable experience)

**Acceptance Criteria:**
- Authentication & Account Management:
  - [ ] User can sign up, verify email, log in, log out, and reset password.
  - [ ] SSO via Google works end-to-end if enabled.
- Core Item CRUD:
  - [ ] User can create, edit, delete items; changes persist in Postgres.
  - [ ] API responses for CRUD ops return <= 200ms p95 under staging load (baseline).
- Sharing & Permissions:
  - [ ] Owner can invite another user and grant read/write; invited user gains access immediately.
  - [ ] Unauthorized requests return 403 and are logged.
- Search & Filter:
  - [ ] Search returns relevant results; first page latency p95 <200ms.
  - [ ] Pagination and basic filters function and are reflected in URLs for shareability.
- Activity Feed & Notifications:
  - [ ] Actions create feed entries visible to participants within 5s.
  - [ ] Email notifications send reliably (retry logic) for invite events.
- Quality & Reliability:
  - [ ] Test coverage >= 80% for core backend services (auth, CRUD, permissions, search).
  - [ ] CI pipeline runs unit tests, linting, and basic integration tests on PRs.
  - [ ] Performance: staging p95 latency across core APIs <200ms; error rate <1%.
- Security & Compliance:
  - [ ] Basic OWASP top-10 mitigations in place (input validation, CSRF, XSS protection).
  - [ ] Secrets stored in vault; DB credentials rotated per policy.

**Out of Scope for MVP:**
- Fine-grained RBAC beyond owner/read/write roles.
- Advanced analytics dashboards.
- Multi-region deployment and hard geo-redundancy (deferred next phase).

**Success Metrics (post-launch):**
- Feature adoption: 60% of active users use Core Item CRUD within 2 weeks.
- Activation: 30% of signups create at least 1 item within 7 days.
- Performance: p95 API latency <200ms in production.
- Quality: 80% test coverage on core services; regression rate <2% per release.

**Dependencies & Constraints:**
- Infra: Postgres (primary DB) + Redis (cache) + Kubernetes on cloud (CEO decision).
- Taylor (#ai-tech-lead) to finalize service boundaries and scaling strategy.
- Noah (#ai-devops) to provision IaC and CI after architecture doc.

**Next Steps:**
- Review and sign-off by Taylor (architecture) and Maya (design) by Thu/Fri.
- Create engineering issues and assign owners (week 0 planning).

**File:** output/specs/mvp_scope.md

Title: Signup & Dashboard UX Spec
Path: output/design/signup_dashboard_spec.md

Summary
- Deliver wireframes and component specs for Signup (email/password) and primary Dashboard screen.
- Focus: clear user onboarding, resilient auth UX (JWT access + refresh rotation), accessibility, and mobile-first responsive layout.

Users & Context
- Primary user: new sign-up user (B2B/B2C early adopter).
- Context: first-time onboarding and then quick access to a personalized dashboard with core actions.

Goals
- Fast, low-friction signup with clear error handling and success path.
- Dashboard that surfaces primary actions and status at-a-glance.
- Designs must be implementable with REST v1 endpoints, OpenAPI-first backend.

Constraints
- Auth flow: JWT short-lived (15m) + refresh (7d) with rotation. Backend will enforce idempotency headers for mutation endpoints.
- Keep forms resilient to network errors and double-submit.
- Responsive: mobile-first, scales to desktop 1024px+.

High-level user flows
1) Signup
  - User enters email + password (confirm optional) -> client shows inline validation -> POST /v1/auth/signup (idempotency header supported) -> on success, receive access + refresh, redirect to onboarding step or dashboard.
  - If email exists: show inline error with CTA to login or reset password.
  - If network error: allow retry with toast and persistent form state.

2) Post-login Dashboard
  - Fetch GET /v1/users/me and GET /v1/dashboard-summary
  - Show top-level status card, primary CTA, recent activity feed, and quick actions.

Component specs
- Form input
  - Label above input, helper text below, error text in red (#D64545). Use aria-describedby linking.
  - Password strength meter (progress bar + label).
  - Primary CTA: full-width on mobile, fixed width on desktop (max 320px).
- Card (Dashboard)
  - Title (H3), metric number, small trend sparkline, optional secondary action (ellipsis menu).
  - Spacing: 16px padding, border-radius 8px, subtle shadow (0 1px 4px rgba(16,24,40,0.04)).
- Top nav / header
  - Left: logo, center: breadcrumb/title, right: avatar + menu
- Notifications / Toasts
  - Slide-in from top-right, accessible (role=alert), auto-dismiss 4s, persistent for critical errors.

Accessibility
- All inputs have labels and aria-invalid when error.
- Error messages announced to screen readers (aria-live="polite").
- Keyboard-first: focus order, focus trap on modals, visible focus outlines.
- Color contrast meets WCAG AA (adjust tokens as needed).

Wireframes (ASCII)
1) Mobile Signup
---------------------------------
| LOGO           Help           |
|                               |
| Sign up                       |
| [Email input            ]     |
| [Password input         ]     |
| (password strength)            |
| [Create account] (primary)    |
| Already have an account? Log in|
---------------------------------

2) Desktop Dashboard (simplified)
-----------------------------------------------------------
| LOGO | Page title                | Avatar    | Notifications|
-----------------------------------------------------------
| [Status Card] [KPI Card] [KPI]  |               |          |
| Recent activity                 | Quick actions |          |
| Larger detail panel (right)     |               |          |
-----------------------------------------------------------

Design decisions / rationale
- Card layout for dashboard: allows scannability and responsive rearrangement. Cards can collapse on mobile to a vertical feed.
- Inline validation: reduces friction and avoids round-trip errors.
- Full-width primary CTA on mobile improves tappability and conversion.
- Use toasts for non-blocking network errors; modal for blocking security prompts (e.g., multi-factor).

API / UX notes for Backend (Marcus)
- Signup endpoint should accept idempotency-key header to prevent duplicate accounts on retries.
- Return consistent errors with field-level error keys (e.g., {"errors": {"email": "already_exists"}}).
- After signup, issue both access and refresh tokens in response body; set secure httpOnly refresh cookie is optional (discuss). Frontend will expect JSON tokens for now.

Implementation notes for Frontend
- Build components in Storybook with tokens for spacing/typography/colors.
- Create a signup page and dashboard page; mock API initially using OpenAPI stubs until feat/api-skeleton is ready.
- Track focus + error states in stories.

Next steps / Handoff
- Frontend: implement components & pages in Storybook; create branch feat/signup-ui and link to backend branch when available.
- Backend: validate idempotency header + field-level error shape.

Files
- This spec: output/design/signup_dashboard_spec.md

Contact
- Ping Maya in #ai-design for clarifications. Marcus please review API/UX notes to ensure fields & error shapes align with OpenAPI.

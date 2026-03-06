Design Spec: Signup + Main Dashboard Flows

Owner: Maya (UX/UI Designer)
Created: 2026-03-06
Purpose: Draft two core UX flows for MVP: (1) Signup (auth) and (2) Main Dashboard (post-login). Intended for #ai-frontend (Kevin) implementation.

High-level goals
- Fast, low-friction signup that supports email + OAuth (Google). Keep required fields minimal.
- Clear primary action on dashboard, progressive disclosure for advanced features.
- Mobile-first, accessible, and implementable components (React + Storybook).

Assumptions & constraints
- Auth uses JWT access + refresh (product decision). The UI must handle token state: loading, refresh flow, signed-out errors.
- Backend: Postgres. Metadata may appear in user profile cards.
- Timeline: Initial draft now; final designs by Wed EOD after feedback.

User Personas
- New User: Wants quick signup, minimal setup.
- Power User: Wants dashboard quick access to key metrics and actions.

Flow 1 — Signup (primary path)
1. Entry points: /signup route, CTA from landing, or OAuth popup.
2. Signup Screen (mobile-first):
   - Header: Product logo left, Login link right.
   - Title: "Create your account"
   - Primary options: "Continue with Google" (OAuth button) then "Or sign up with email" divider.
   - Email form: Email (required), Full name (optional), Password (required, progressive strength meter), Accept TOS checkbox.
   - CTA: Primary button "Create account" (disabled until required fields valid).
   - Inline error messages under fields; general error banner top for system errors.
3. Post-submission:
   - Show a short onboarding modal (3 slides) or skip link.
   - Redirect to /dashboard after email verification OR immediate access with limited features (show verification reminder).
4. Edge cases:
   - Existing account: show error with "Log in" CTA.
   - OAuth conflict: detect existing email and offer account linking.

Components (Signup)
- OAuthButton: icon, label, full-width, 48px tall, accessible color contrast.
- Field: label, placeholder, helper text, inline validation message, aria-describedby support.
- PasswordMeter: inline strength + tooltip with tips.
- FormLayout: single-column, 16px vertical gap, max-width 420px centered on desktop.

Wireframe (ASCII)
[Header: logo | Log in]

[ Create your account ]
[ Continue with Google             ]
[ — Or sign up with email — ]
[ Email                 ]
[ Full name             ]
[ Password [•••••] ] [strength meter]
[ ☑ I agree to Terms ]
[ Create account ]
[ Already have an account? Log in ]

Accessibility notes
- All form elements keyboard focus visible.
- Buttons have aria-label where icon-only.
- Color contrast >= 4.5:1 for body text.

Flow 2 — Main Dashboard
Goals: deliver immediate value; primary CTA prominent; secondary info discoverable.
Entry: after login or persisted session.

Information architecture (mobile-first)
- Top Nav: hamburger (left), product logo center, user avatar (right) with quick menu.
- Primary area (vertical stack):
  1) Global status card (metrics snapshot): primary KPI + small sparkline.
  2) Quick actions row: up to 3 prominent CTAs (e.g., New Item, Import, Connect).
  3) Activity feed / recent items (card list) — default collapsed to 3 items with "See more".
  4) Secondary panels (foldable): Settings summary, Integrations.

Layout details
- Container: 16px margins on mobile, max-width 1100px on desktop with 24px side gutters.
- Cards: subtle elevation, 12px border-radius, 16px internal padding.
- Typography: H1 20/28, H2 16/22, Body 14/20, Button 14/16.

Primary components
- KPI Card: title, big number, delta (green/red), sparkline small.
- QuickAction Button: icon + label, 44px height, primary color for main action.
- ListItem Card: title, meta row, action overflow (⋯) for item actions.
- Empty state illustrations with short CTAs.

Wireframe (mobile)
[TopNav: ≡   Product   ○ ]
[KPI card: Users 1,234  +3% ]
[ Quick actions: [New] [Import] [Connect] ]
[ Recent items: Card 1 | Card 2 | Card 3 ]
[ See more ]
[ Panels: Settings ▸ | Integrations ▸ ]

Interactions
- QuickAction opens modal — modal header + primary CTA at top-right.
- Cards support swipe-to-delete on mobile (confirm toast) and long-press for reordering (optional).
- All list items lazy-load when "See more" clicked.

Design decisions & rationale
- Mobile-first: majority of early users expected on mobile; ensures responsive baseline.
- Card-based layout: visual grouping, easy to scan, straightforward to implement with CSS Grid.
- Minimal signup fields: reduces drop-off — we can collect additional metadata later in profile.
- OAuth first option: reduces friction and improves conversion.

Developer handoff notes
- Provide Storybook stories for: OAuthButton, Field, PasswordMeter, KPI Card, QuickAction, ListItem Card.
- Use tokens for spacing/typography/colors. I'll supply a small style token set on next iteration.
- Auth UI must expose hooks for token errors (expired, invalid) — show banner with re-login CTA.

Next steps
1. Kevin: implement components in React + Storybook (see next_steps below).
2. I will iterate on visuals and deliver tokens by Wed EOD.

Files created
- This spec: output/design/signup_dashboard_flows.md

Open questions
- Do we require email verification before granting dashboard access or allow immediate access with soft-blocks?
- Which OAuth providers besides Google should we include for MVP?



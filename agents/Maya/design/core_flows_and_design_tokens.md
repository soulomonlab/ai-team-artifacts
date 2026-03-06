# Core Flows & Design Tokens (MVP)

Owner: Maya (Designer)
Created: 2026-03-06

Purpose
- Deliver core user flows and initial design tokens for web + mobile MVP.
- Focus: usability, accessibility, and implementability within 8-week target.

Scope (MVP UX)
- Onboarding / Signup
- Primary task flow (create -> edit -> share)
- Main dashboard / list view
- Search & filter
- Settings & profile
- Error & empty states

Key decisions
- Mobile-first responsive design (breakpoints: 375, 768, 1200).
- Card-based list layout for visual hierarchy and scannability.
- Primary action as floating CTA on mobile; top-right CTA on desktop.
- Accessibility: WCAG AA contrast min, 14px body on mobile baseline.
- Use system fonts stack for performance: Inter / -apple-system / Roboto.

Design Tokens (initial)
- Colors:
  - primary: #0066FF
  - primary-600 (hover): #0052CC
  - accent: #00C2A8
  - background: #FFFFFF
  - surface: #F6F7FB
  - text-primary: #0B1220
  - text-secondary: #6B7280
  - danger: #E03E3E

- Typography:
  - display-1: 32px / 40px / 600
  - heading-2: 20px / 28px / 600
  - body: 16px / 24px / 400
  - caption: 12px / 16px / 400
  - line-height values included above

- Spacing (8pt scale):
  - xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px

- Elevation / shadows:
  - card: 0 1px 3px rgba(11,18,32,0.04)
  - modal: 0 8px 24px rgba(11,18,32,0.12)

Core Components (specs)
- App Shell: top nav (desktop), bottom nav (mobile), left nav optional on desktop for power users.
- Card (list item): 16px padding, border-radius 12px, surface background, avatar/icon left, title + subtitle.
- Primary Button: height 44px, border-radius 10px, uses primary color, left-aligned icon optional.
- Floating Action Button (mobile): 56px circle, primary, bottom-right.
- Form inputs: 48px height, 12px vertical padding, subtle border, error state with danger color.

User Flows (high level)
1) Onboarding / Signup
   - Entry → Feature highlights (2 screens) → Create account (email/OAuth) → Quick tour → Dashboard
   - Decision: keep signup minimal (email + name) to reduce friction.

2) Primary task flow (Create → Edit → Share)
   - Dashboard (list) → Tap + (FAB) → Create modal/screen → Save (optimistic UI) → Item detail → Edit inline or open editor → Share (link / invite)
   - Autosave: yes (local + backend) to avoid data loss.

3) Search & Filter
   - Persistent search at top of list, filters accessible by dropdown modal. Results highlight query terms.

Wireframes (ASCII)
- Mobile: Dashboard list

  [Top Bar: Logo | Search Icon]
  -------------------------------
  | CARD 1                     >|
  | title                     |
  | subtitle                  |
  -------------------------------
  | CARD 2                     >|
  -------------------------------
  [FAB +]    [Bottom Nav: Home / Create / Profile]

- Desktop: Dashboard + left nav

  [Left Nav] | [Top Bar: Search | Actions]
  ------------------------------
  | CARD GRID (2-col)           |
  | title / subtitle / actions  |
  ------------------------------

Accessibility notes
- Color contrasts checked for primary & text. If new colors added, verify AA.
- Interactive targets >= 44x44 dp on mobile.
- All images must include alt text.

Open questions / blockers
- Final MVP feature list from Alex (needed to finalize screens + flows).
- Analytics / events naming agreed with Data team (Samantha) to map interactions.

Next steps
- Iterate screens after Alex finalizes top features (EOD Tue).
- Deliver clickable Figma frames + assets by Fri.

Files created
- This spec (output/design/core_flows_and_design_tokens.md)

Ask for frontend
- Kevin (#ai-frontend): please review tokens & component specs for feasibility. Early feedback by Tue EOD helps keep dev schedule.


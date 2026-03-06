Title: Initial Wireframe Requirements & Decisions
Path: output/design/wireframe_requirements.md

Purpose
- Capture design assumptions, required screens, component specs, and initial low-fidelity wireframes so frontend/back can proceed once PRD is ready.

When I'll deliver final wireframes
- I will produce detailed mobile + desktop wireframes (annotated) after Alex finishes PRD (output/specs/initial_prd.md).

Key decisions (preliminary)
- Layout: Card-based list for primary content (scannable, supports thumbnails + meta)
- Navigation: Top global nav (logo, search, user menu), contextual sub-nav for feature flows
- Primary CTA: Prominent, filled button; place top-right desktop, bottom-right FAB on mobile
- Forms: Inline validation, single-column mobile forms, two-column desktop where space permits
- Auth flows: Smooth modal progressive disclosure; show short session TTL warning in-app for access-token expiry
- Accessibility: WCAG AA colors, 16px base font, 4.5:1 contrast for body text
- Responsiveness: Breakpoints: 375 (mobile), 768 (tablet), 1024 (desktop)

Required screens (MVP)
1. Landing / Dashboard (authenticated)
2. Resource list (card/grid) with cursor paging controls
3. Resource detail (actions: edit, delete, share) + caching indicator
4. Create / Edit modal / page (idempotency note for POST)
5. Auth: Sign-in, Refresh notice, Session expired flows
6. Settings / Profile (RBAC-aware controls)
7. Empty / error / rate-limit states

Component specs (high level)
- Card: thumbnail 72x72, title, meta row (muted), actions menu (ellipsis)
- List controls: Limit selector, cursor-scroll indicator, fallback page input
- Modals: Max-width 720px desktop, full-screen modal on mobile
- Toasts/alerts: top-right transient; error details link expands

Wireframes (low-fidelity ASCII)
- Desktop: Dashboard
  ------------------------------------------------------------
  | LOGO | Search [_________] | Notifications | Avatar [v]      |
  ------------------------------------------------------------
  | Sub-nav: All | My Items | Create [+]                       |
  ------------------------------------------------------------
  | Card 1  | Card 2  | Card 3  |                              |
  | Title   | Title   | Title   |                              |
  ------------------------------------------------------------
  | ← older (cursor)               •  •  •                 Next →|
  ------------------------------------------------------------

- Mobile: Resource list
  ---------------------------------
  | LOGO | [Search icon] | Avatar |
  ---------------------------------
  | Sub-nav: All ▾                         |
  ---------------------------------
  | [Card]                                 |
  | Title                                  |
  | meta • actions                         |
  ---------------------------------
  | FAB (+) bottom-right                   |
  ---------------------------------

Questions / blockers for PRD
- Primary user persona(s)? (Admin / End-user / Both)
- Critical flows: is offline-first needed? push notifications?
- Any branding guidelines (colors, fonts) to use now?
- Are there specific RBAC roles to visualize in settings?

Next steps (from design)
- After PRD: deliver full annotated wireframes for mobile + desktop and a small component library (colors, typography, spacing) → output/design/wireframes_mvp.md
- I'll sync with #ai-frontend (Kevin) once wireframes ready.

Notes for backend (Marcus)
- I'll reflect cursor-based paging in the list wireframes (show cursors, limit selector)
- Show rate-limit UI (toasts) and session/refresh UX for short tokens

File created by: Maya (Designer)

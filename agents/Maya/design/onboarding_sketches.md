Title: Onboarding + Core Task Flow — Mid-Fidelity Specs
Author: Maya (UX/UI)
Date: 2026-03-04

Overview
- Deliverables: 2 mid-fi screens (Onboarding flow, Core Task flow) specification, component inventory, user flows, wireframes (ASCII), design decisions and accessibility notes.
- Next: I'll produce a PDF with visual mockups within 4 business days (by 2026-03-10). This markdown is the handoff spec to start frontend planning.

Key decisions (made)
- Clean card-first layout for tasks: improves scanability and works well across mobile & desktop.
- Primary actions: filled primary color, secondary actions: outline. Clear affordance for "Create" and "Complete".
- Onboarding kept to 3 screens max (Welcome -> Account -> Preferences) to minimize drop-off.

User personas & context
- Persona: Busy professional, needs to create/manage tasks quickly on web and mobile.
- Context: First-time user (onboarding) and returning user (core flow) on both desktop and mobile.

User Flows (mermaid)
```mermaid
flowchart TD
  A[Landing / Welcome] --> B[Sign up / Login]
  B --> C[Preferences (3 toggles + timezone)]
  C --> D[Quick Tour (skip-able)]
  D --> E[Task List (Home)]

  E --> F[Create Task]
  F --> G[Task Detail]
  G --> H[Mark Complete / Edit / Delete]
```

Onboarding Screens — Mid-fi Wireframes
1) Welcome
- Purpose: orient & convert
- Components: App header (logo), headline, 3 bullet benefits (icons), CTA primary "Get started", CTA secondary "Sign in"
- Copy (example): "Organize your day. Start in 60 seconds."
- States: initial, error (if sign-up failed), small-screen responsive -> stacked bullets

ASCII wireframe
---------------------------------
| LOGO            [Sign in]      |
|--------------------------------|
| Headline: Organize your day     |
| - Benefit 1  - Benefit 2        |
| - Benefit 3                     |
| [Get started]   [Sign in]       |
---------------------------------

2) Sign up / Account
- Purpose: minimal friction signup
- Fields: Email, Password (show/hide), Name (optional)
- Validation: client-side inline for email format + password strength
- Components: input fields, password strength meter, continue CTA (primary), back link
- Accessibility: label + aria-describedby for errors

ASCII wireframe
---------------------------------
| < Back                         |
| Headline: Create your account  |
| [Email]                        |
| [Password] [strength meter]    |
| [Name (optional)]              |
| [Continue]                     |
---------------------------------

3) Preferences
- Purpose: capture minimal preferences for tailoring UX
- Options: Default view (List/Card), Notifications (Email/Push), Timezone
- Components: toggles, dropdown, CTA Finish
- Decision: keep third step light (< 5 inputs) to reduce friction

Core Task Flow — Mid-fi Wireframes
1) Task List (Home)
- Layout: top nav, left filter/quick actions (desktop) or bottom sheet (mobile)
- Main: list of task cards with title, due, priority chip, assignee (if team), quick checkbox to mark complete
- Empty state: illustration + CTA "Create first task"
- Filters: All / Today / Overdue / Completed

ASCII wireframe (desktop)
-----------------------------------------------
| LOGO | Search [____] | Create Task [ + ]    |
|---------------------------------------------|
| Sidebar: Filters |  Task cards (3-column)   |
|                 |  Card: Title            |
|                 |        Due • Priority   |
|                 |  [checkbox] Quick actions|
-----------------------------------------------

2) Create Task (modal)
- Fields: Title (required), Description (optional), Due date, Priority, Add assignee, Tags
- Actions: Save (primary), Cancel (ghost)
- Validation: inline; title required

3) Task Detail (panel/modal)
- Shows full description, activities, attachments, comments
- Actions: Edit, Complete, Delete
- Accessibility: keyboard trap in modal, focus management, aria-live for updates

Component Spec (high level)
- Buttons
  - Primary: filled, brand color (action), 16px padding, 8px radius
  - Secondary: outline, same height
- Inputs
  - Height: 44px desktop, 40px mobile; labels above inputs; placeholder + label
- Cards
  - Elevation: 1 (subtle shadow), 12px padding, 8px border radius
  - Priority chips: small rounded badges (colors red/yellow/green)
- Toggles & Dropdowns: native-select fallback; custom accessible toggles

Color & Typography (starter)
- Primary: #2563EB (blue)
- Secondary: #6B7280 (muted)
- Background: #FFFFFF
- Surface: #F9FAFB
- Type: Inter (System fallback: -apple-system, Roboto)
  - H1: 24px / 600
  - H2: 18px / 600
  - Body: 14px / 400

Accessibility Notes
- Contrast ratios: ensure primary action > 4.5:1 vs background
- Keyboard: all actions reachable, modals trap focus, skip-to-content
- Forms: inline error messaging, aria-live for success notifications

Responsive considerations
- Breakpoints: mobile < 640px, tablet 640-1024px, desktop >1024px
- Sidebar collapses to bottom sheet on mobile
- Card grid reduces columns with screen width

Open questions / clarifying needs
- Branding: confirm final primary color + logo assets from #ai-design (or brand).
- Any required social sign-in providers (Google/Apple)? I left generic email first.

Handoff & Next steps
- I'll produce 2 mid-fi mockups (PDF + PNGs) by 2026-03-10.
- Handoff: #ai-frontend — please prepare component list from this spec and call out feasibility concerns.
- #ai-docs — Emma, I'll need final copy for onboarding CTAs before PDF export.

Files created: this spec (markdown). Visuals to follow.


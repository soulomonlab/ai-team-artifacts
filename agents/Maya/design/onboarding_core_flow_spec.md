# Onboarding + Core Flow Design Spec

Owner: Maya (UX/UI)
Created: 2026-03-04

Purpose
- Deliver onboarding screens and core app flow for initial QA visual tests and frontend implementation.
- Focus: clarity, progressive disclosure, fast time-to-value.

Files
- output/design/onboarding_core_flow_spec.md (this file)

User & Context
- Primary user: Productive knowledge worker who wants quick setup and immediate value (5-10 min). 
- Constraint: First-time users should complete onboarding in <5 minutes and reach the core task (create/search) within 2 taps.

High-level flows
1) Lightweight onboarding (required)
   - Welcome (value prop + CTA)
   - Account creation / SSO or continue as guest
   - Quick preferences (1 screen; skip allowed)
   - Guided first task (in-product micro-tutorial)
   - Completion -> Home (core flow)

2) Core flow (primary task path)
   - Home / Dashboard (search bar, recent items, recommended actions)
   - New Item / Create (modal or full screen depending on context)
   - Results / Item List (card layout with actions)
   - Item Detail / Edit (side panel on desktop, full screen on mobile)

User Flow Diagram (mermaid)

```mermaid
flowchart LR
  A[Welcome] --> B[Account setup / SSO]
  B --> C[Preferences (optional)]
  C --> D[Guided first task]
  D --> E[Home / Dashboard]
  E --> F[Create new item]
  E --> G[Search / Results]
  G --> H[Item Detail]
```

Wireframes (ASCII)

1) Welcome
-------------------------------------------------
| LOGO            Welcome to AppName             |
|                                            [X] |
|  Big headline: "Get useful results in minutes"   |
|  Short blurb explaining key value                 |
|                                                  |
|  [Sign in with SSO]  [Continue as guest]         |
|  Small: "Already have an account? Sign in"      |
-------------------------------------------------

2) Preferences (single-screen)
-------------------------------------------------
| Progress: ●○○    Headline: Customize your experience |
|  - Primary goal: [dropdown]                         |
|  - Data sharing toggle: [on/off]                    |
|  [Skip for now]           [Save & continue]        |
-------------------------------------------------

3) Home / Dashboard (desktop)
-------------------------------------------------
| Top Nav: Logo | Search [___________] | Profile ▾    |
| --------------------------------------------------- |
| [Create New]  [Recommended action cards]            |
| Recent items:  Card  Card  Card                      |
| Footer: Tips / Support link                          |
-----------------------------------------------------

4) Create modal (mobile)
---------------------------------
| X  Create New                     |
| Title [________]                  |
| Template: [Select]  [Suggest]     |
| CTA: [Create]  [Cancel]           |
---------------------------------

Component specs
- Nav/Header: height 56px desktop, 48px mobile; primary CTAs on right; search should be prominent and support typeahead.
- Primary Button: filled, primary color #0A64FF, white text, 12px border-radius, padding 10px 16px.
- Secondary Button: outline, border #D6E4FF, text #0A64FF.
- Card: elevation 1 (subtle shadow), border-radius 8px, padding 12px. Title 16px medium, body 14px.
- Modal: centered on desktop, full-screen sheet on mobile, close in top-right.

Accessibility
- All interactive elements: min 44x44 tap area.
- Contrast ratios: buttons and text meet WCAG AA (primary text contrast at least 4.5:1).
- Use semantic HTML (header, nav, main, dialog) for screen readers.

Responsive rules
- Breakpoints: mobile < 640px, tablet 640–1024px, desktop >1024px.
- Card grid: mobile 1 column, tablet 2 columns, desktop 3 columns.
- Item detail: slide-over on desktop, full-screen on mobile.

Design decisions (why)
- Card layout for results: visual hierarchy and scannability for mixed-content results.
- Single-screen preferences: reduces drop-off vs multi-step forms; allow skip to respect power users.
- Guided first task (in-product micro-tutorial): increases activation and reduces support load.

Handoff notes for #ai-frontend (Kevin)
- Key screens: Welcome, Preferences, Home, Create modal, Item detail.
- Assets: Provide SVG icons + 48px/24px exports. I'll upload illustrations if you want them — confirm asset formats.
- Interaction details: typeahead should debounce at 200ms; search suggestions as a dropdown.
- Accessibility: use ARIA roles for dialogs and ensure focus trap in modals.
- Implement tokens: primary #0A64FF, surface #FFFFFF, neutral-100 #F4F6FB.

Handoff notes for #ai-qa (Dana)
- Please create visual regression checks for: Welcome, Preferences, Home (empty and populated), Create modal, and Item detail.
- Primary acceptance: onboarding completes within 5 minutes; first task success rate during smoke tests >90%.

Open questions / blockers
- Do we need custom illustrations now or can we use placeholders for initial QA? (I prefer placeholders to unblock).
- Confirm brand color tokens from product — I've proposed primary #0A64FF; change if needed.

Next steps
- I'll export a small set of SVG placeholders and a Figma link if needed. Tell me preferred asset format.
- #ai-frontend please start implementing screens. #ai-qa — you can start writing E2E visual checks against these screens.


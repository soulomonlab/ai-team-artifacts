# Onboarding + Core Flow Design Spec

Path: output/design/onboarding_coreflow_spec.md

Owner: Maya (UX/UI)
Date: 2026-03-04

Purpose
- Deliver onboarding screens + core user-flow wireframes and component specs for implementation.
- Focus: fast activation (first-success within 60s), mobile-first, accessible, easy to implement.

Deliverables
- Wireframes (ASCII + mermaid flow)
- Screen list & brief descriptions
- Component specs (spacing, states, microcopy)
- Color & typography tokens (proposal)
- Interaction notes & accessibility
- Implementation handoff note for #ai-frontend

User & Context
- Primary user: new users on mobile web / mobile app wanting to set up and perform core action quickly.
- Constraint: Backend/API not final — design uses optimistic UI and clear loading/error states.

User Flow (mermaid)

```mermaid
flowchart TD
  A[Welcome / Landing] --> B{Sign up or Log in}
  B -->|Sign up| C[Email / Social auth]
  B -->|Log in| D[Login screen]
  C --> E[Set up profile (1 screen)]
  E --> F[Quick product tour (2 slides, skipable)]
  F --> G[Core home / dashboard]
  G --> H[Create / Primary action]
  H --> I[Success state]
```

Screens to deliver
1. Welcome / Landing
   - CTA: Get started (primary) and Log in (secondary)
   - Subtle product value 1-liner
2. Sign up (email + social) — combined to reduce steps
   - Inline validation
3. Login — password + social
   - Forgot password link
4. Profile setup (single progressive screen)
   - 2 fields max (name, role) + avatar skip
5. Quick tour (2 cards, skip option)
6. Core home / dashboard
   - Primary action FAB or prominent CTA
   - Recent items list (card layout)
7. Create / Primary action flow (2 screens: form + confirm)
8. Success / Empty state with next-step CTA

Wireframes (mobile portrait ASCII)

Welcome
+------------------------------------------------+
|  Logo                                         |
|                                                |
|  Headline: "Get started in under a minute"   |
|  Subtext: one-line value prop                  |
|                                                |
|  [Get started (primary)]                       |
|  [Log in (secondary)]                          |
+------------------------------------------------+

Core Home
+------------------------------------------------+
| Top nav (title + profile)                      |
|                                                |
|  [Search bar]                                  |
|  Recent                                    >   |
|  - Card 1 (title, subtitle, action)            |
|  - Card 2                                      |
|                                                |
|                      [ + Create ] (FAB)        |
+------------------------------------------------+

Component specs (key)
- Buttons
  - Primary: height 48px, radius 12px, padding 16px, bold 16/18px
  - Secondary: ghost with border
  - Disabled state: 50% opacity
- Inputs
  - Height 44px, radius 10px, placeholder color #9AA0A6
  - Error: 1px red border + inline message
- Cards
  - Padding 12px, radius 10px, elevation: subtle shadow
- FAB
  - Size 56px circular, bottom-right spacing 16px

Color & typography (tokens)
- Primary: #0A84FF (blue)
- Accent / Success: #00C853
- Neutral 900: #111827, Neutral 500: #6B7280
- Error: #EF4444

Typography
- System font stack (mobile): Inter / -apple-system / Roboto
- Headline: 20px / 600
- Body: 16px / 400
- Small: 13px / 400

Accessibility
- Contrast: ensure primary text >= 4.5:1
- Touch targets >= 44px
- Keyboard & screen-reader labels for all fields
- Motion: reduce-motion support

Decisions / Rationale
- Mobile-first: majority initial users are mobile. Keeps scope focused.
- Combined sign-up/login flow reduces drop-off.
- Minimal profile setup: remove friction — collect only what's needed.
- Card layout chosen for scannability on small screens.

Hand-off & Next steps
- I'll export screens (PNG + SVG) and add to output/design/assets/ by EOD tomorrow.
- Handoff notes for #ai-frontend: implement tokens above, use accessibility states, provide loading & error mocks.
- Blockers / Questions for product:
  1) Target platforms: web + native iOS/Android? (confirm priorities)
  2) Brand colors / logo files (if available)

Files created now
- This spec: output/design/onboarding_coreflow_spec.md

Implementation request
- #ai-frontend please review and flag feasibility/unknowns. I'll drop exported assets by EOD tomorrow.

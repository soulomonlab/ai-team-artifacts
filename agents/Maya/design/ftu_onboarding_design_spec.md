Title: First‑Time User Guided Onboarding (FTU Onboarding) — Design Spec
Path: output/design/ftu_onboarding_design_spec.md

Overview
- Purpose: Design a lightweight 3‑step guided onboarding to increase activation (+15–25% within 7 days).
- Scope: Web (desktop + mobile responsive). In‑app flow shown at first sign-in; option to dismiss/snooze.
- Success metrics: Activation rate (key action completion within 7 days), FTU completion rate, time to complete.

User & Context
- Primary: New users who just signed up and have not completed the key action.
- Environment: First session after signup, may be on mobile or desktop, short attention span.

High‑level flow (3 steps)
1) Welcome & primary value: explain the one key action and why it matters. CTA = "Get started".
2) Guided setup: 1–2 micro‑tasks (config/first content) with optional help tips.
3) Confirmation + next steps: celebrate completion, show progress, CTA to main product.

A/B Test
- Variant A (FTU): show 3‑step flow
- Variant B (Control): current default (no guided flow)
- Randomize on signup; track cohort conversion to activation within 7 days.

Wireframes (ASCII)
- Entry (coachmark modal, centered)
+-----------------------------------------+
| Logo        Welcome to ProductName      |
|                                          |
|  Headline: "Get set up in 3 quick steps" |
|  Sub: "We’ll guide you to your first win"|
|  [Get started]        [Skip]             |
+-----------------------------------------+

- Step (inline card stacked, progress 1/3)
+-----------------------------------------+
|  • Progress: Step 1 of 3                 |
|  Headline: Connect X                      |
|  Body: Short instruction                  |
|  [Complete task]     [Help]               |
+-----------------------------------------+

- Completion
+-----------------------------------------+
|  ✅ You're all set!                        |
|  Headline: "You completed setup"         |
|  CTA: "Go to Dashboard"                  |
+-----------------------------------------+

Component specs
- Modal container: centered, max‑width 720px (desktop), full width on mobile, accessible focus trap.
- Progress indicator: short "Step X / 3" + small horizontal progress bar.
- Primary CTA: filled, primary color; Secondary CTA: text button.
- Micro‑task card: title, 1–2 line description, optional inline input or connector button, subtle help icon.
- Contextual tips: small tooltip anchored to relevant elements, dismissible per session.

Copy (recommended microcopy)
- Entry headline: "Get set up in 3 quick steps"
- Step 1 title: "Create your first X"
- Step 1 action: "Create X"
- Step 2 title: "Invite a teammate (optional)"
- Completion: "Nice! Your workspace is ready."

Accessibility & Edge cases
- Keyboard nav and screen‑reader labels for all controls.
- Skip/dismiss must be persistent ("Do not show again") for users who opt out.
- If user leaves mid‑flow, resume on next session with subtle nudge.

Analytics (events & attributes)
- ftu.shown {user_id, variant, timestamp}
- ftu.step_shown {user_id, step, timestamp}
- ftu.step_completed {user_id, step, timestamp}
- ftu.completed {user_id, total_time, steps_completed}
- activation.completed {user_id, within_7d=true/false}

Design decisions (key)
- 3 steps chosen to minimize friction and maximize perceived progress.
- Modal entry preferred to ensure visibility; inline resume on subsequent sessions to reduce interruption.
- Use a progress indicator to increase completion rates (psychology evidence).

Implementation notes for frontend
- Provide hooks for analytics events above.
- Expose simple variant flag (ftu_variant) to toggle flow.
- Mobile responsive: modal becomes full‑screen sheet on narrow viewports.

Next steps / handoff
- Design deliverable created here: output/design/ftu_onboarding_design_spec.md
- Frontend (Kevin): implement UI, analytics hooks, A/B toggles.
- Backend (Marcus): finalize event contract and lightweight endpoints if needed (e.g., track server‑side activation).
- QA (Dana): test happy path + mid‑flow exit/resume + A/B measurement.

Rationale summary
- Prioritize UX to boost activation quickly; simple flow with measurable events supports A/B testing and rapid iteration.

Files & assets
- This spec (detailed copy + wireframes). Visual mockups can be added on request.


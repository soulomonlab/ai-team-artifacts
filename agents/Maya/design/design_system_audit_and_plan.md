Design System Audit — MVP Gap Analysis & Plan

Summary
- Goal: Audit current design system for gaps vs. MVP priorities (activation-focused UX).
- Output: shortlist of gaps, quick fixes (this sprint), and required component specs.

Existing (observed)
- Color tokens: primary, neutral, danger defined
- Typography: H1..H4 + body, but inconsistent scaling on mobile
- Buttons: Primary/Secondary available; no subtle/tertiary styles
- Forms: basic inputs exist; no validation/inline help patterns
- Icons: partial set; no illustrations library
- Grid/Spacing: desktop-first; mobile constraints not fully specified

Gaps vs. MVP needs (high impact)
1) Onboarding & First-Run Patterns
   - Missing: progressive steps, progress indicator, contextual microcopy.
   - Why it matters: activation rate depends on clarity in first 2 mins.
2) Actionable Home/Dashboard Components
   - Missing: activation card, empty state patterns, quick actions.
   - Why: drives activation and discoverability.
3) Create Flow (primary conversion flow)
   - Missing: stepper, inline validation, smart defaults.
   - Why: reduces drop-off in core task completion.
4) Responsive tokens & spacing
   - Inconsistent mobile type scale and hit targets <44px in some controls.
5) Accessibility checklist
   - No AA contrast validations or keyboard states in docs.
6) Visual assets (icons/illustrations)
   - Need consistent style for hero/empty states.

Quick-fix priorities (this sprint)
- Provide mobile type scaling tokens and spacing map (P1)
- Create activation CTA component + empty state cards (P1)
- Define stepper + form validation patterns for create flow (P1)
- Add AA contrast checks for primary/secondary (P2)

Deliverables I'll produce by Tue
- 3 key screens: Onboarding (first-run), Home/Dashboard (activation-focused), Create Flow (core conversion)
- Component specs: Activation CTA, Stepper, Empty State, Inline Validation
- Recommendations doc (this file) with implementation notes for frontend

Key decisions (design)
- Use card-based layout for dashboard to make affordances scannable (decision: cards -> faster comprehension)
- Primary CTA persistent in header and as sticky FAB on mobile for quick access
- Minimal hero illustrations for friendliness, but keep load small (SVG icons)

Next steps / Hand-off
- #ai-frontend (Kevin): Implement screens + components. I will provide specs + assets. Please confirm: React + Tailwind tokens OK?
- #ai-product (Alex): Review microcopy for onboarding steps (I'll add placeholders)

Files produced: output/design/design_system_audit_and_plan.md

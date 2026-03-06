# Figma Screen Variations & Interaction Notes

Owner: Maya (UX/UI Designer)
Deliverable: 3 screen variations + interaction notes (mobile + desktop)
Deadline: Thu COB (as requested)

---

## Context
Goal: Deliver three high-quality visual and interaction directions for the primary product screens so the team can pick a direction for implementation. Focus on clarity, quick discovery, and responsive behavior.

Primary user: busy professional who needs quick access to insights and actions. Use contexts: 1) quick glance on mobile; 2) deeper task flow on desktop.

Assumptions / constraints:
- Will be handed to frontend (#ai-frontend) to convert to Figma and implement.
- Use existing design system tokens where possible (we'll document component specs below).

---

## User flow (high level)
1. Landing / Dashboard: summary cards + quick actions
2. Detailed view: list/table + filters + item detail panel
3. Item creation / edit modal

Key interactions: filters persist between views; quick actions accessible from cards; item detail slides over on desktop, modal on mobile.

---

## Variation A — "Card-first (Focused)"
Principle: Emphasize high-priority items with prominent cards and large CTAs.

Desktop wireframe (ASCII):
[Header]
[Left nav | Main: Large summary cards stacked 2-column | Right: activity feed]

Mobile wireframe:
[Header]
[Summary carousel]
[List of items]

Interaction notes:
- Cards show 3 quick actions on hover (desktop) and on long-press (mobile).
- Primary CTA on each card: one-tap action. Secondary actions in overflow menu.
- Accessible color contrast for status chips.

Use when: users need quick, action-oriented overview.

---

## Variation B — "Data-dense (List & Filters)"
Principle: Maximize scannability for power users — list/table with inline controls.

Desktop wireframe:
[Header]
[Left: Filters panel | Main: Data table with expandable rows | Right: detail panel]

Mobile wireframe:
[Header with filter chip]
[Compact list — each row tappable to open detail modal]

Interaction notes:
- Desktop: expandable rows reveal inline actions (edit, assign, quick comment).
- Filters are sticky and collapsible. State saved in local storage.
- Keyboard shortcuts for power users (to be documented separately).

Use when: power users with high throughput and filtering needs.

---

## Variation C — "Hybrid (Balanced)"
Principle: Balance visual clarity and density. Cards at top, list below.

Desktop wireframe:
[Header]
[Top: compact summary cards (1 row)]
[Below: content area with list + optional right detail rail]

Mobile wireframe:
[Header]
[Compact cards horizontally scrollable]
[Condensed list]

Interaction notes:
- Detail opens in right rail on desktop, full screen on mobile.
- Progressive disclosure: show essential metadata in list, more in detail rail.

Use when: mixed audience with both glanceable and in-depth needs.

---

## Component specs (high level)
- Header: height 64px desktop, 56px mobile. Contains search, user menu, global actions.
- Left nav: 240px collapsed to 72px icons (desktop only).
- Cards: 16px padding, 12px corner radius, elevation 100 (subtle). Title 16/24 weight.
- List rows: height 56px (compact) / 72px (comfortable). Tap area >=44x44.
- Buttons: Primary (#primary), Secondary (ghost). Provide tokens in token doc.
- Colors & typography: Refer to design system tokens. Ensure 4.5:1 contrast for body text.

Spacing: base 8px grid. Use multiples for margin/padding.

Accessibility: keyboard focus states, screen reader labels for actions, ARIA roles for lists and dialogs.

---

## Responsive rules
- Breakpoints: mobile < 768px, tablet 768–1024px, desktop > 1024px.
- Desktop detail: right rail 360–420px. Mobile detail: full-screen modal.

---

## Decision rationale (summary)
- Card-first: best for task-oriented users who need quick actions.
- Data-dense: best for power users; trades visual polish for throughput.
- Hybrid: safest middle ground for mixed audience; less risky for adoption.

Recommendation: Start with Variation C (Hybrid) as default; build A as alternative for mobile-first flows and B for admin/power UX.

---

## Deliverables for #ai-frontend (Kevin)
1. Convert chosen variation to Figma screen files (desktop + mobile) — include component instances.
2. Implement responsive layout rules and provide CSS tokens mapping.
3. Flag any technical constraints (e.g., virtualization needed for large lists).

---

## Next steps & timeline
- Today: Design owner (Maya) provides these specs.
- By Thu COB: I will produce Figma files for top-chosen variation if #ai-frontend requests it.

---

Files created: output/design/figma_screen_variations_spec.md

Questions for the team:
- Marcus: any backend constraints on live-updating cards (WebSocket vs polling)?
- Kevin: which variation do you prefer to prototype in Figma first? I recommend Hybrid.


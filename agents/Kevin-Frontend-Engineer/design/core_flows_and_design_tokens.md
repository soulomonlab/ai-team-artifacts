# Core Flows and Design Tokens (MVP)

Mobile-first, card-based layout. Primary FAB for main action on mobile. Tokens include colors, typography, spacing. Accessibility and autosave decisions included.

## Tokens
- Colors:
  - primary: #0066FF
  - primary-600: #0066FF
  - primary-700: #0052CC
  - gray-50: #F9FAFB
  - gray-100: #F3F4F6
  - gray-200: #E5E7EB
  - gray-300: #D1D5DB
  - gray-500: #6B7280
  - gray-900: #111827
- Typography:
  - base: 16px
  - scale: 12/14/16/18/20/24
  - font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial
- Spacing:
  - xs: 4px
  - sm: 8px
  - md: 16px
  - lg: 24px
  - xl: 32px

## Components (spec-high level)
- AppShell: header (back + title), main content container (max-width 640px), mobile footer nav
- Card: tappable area with a11y (role=button if clickable), title, subtitle, optional body
- PrimaryButton: solid / outline variants, disabled state, focus ring
- FAB: fixed bottom-right, circular, accessible label

## Accessibility Decisions
- Tappable targets >=44px
- High contrast for primary color
- Keyboard support for tappable cards
- ARIA labels for FAB and icon-only buttons

## Autosave
- Drafts autosave every 5s after change (debounced 1s) — note: backend needs draft endpoint

## Open Questions
- Final MVP feature list from Alex (blocks screens like Settings)
- Analytics event mapping from Samantha (which events to instrument)
- Backend pagination format for list screens (offset vs cursor)


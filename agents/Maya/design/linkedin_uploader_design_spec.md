# LinkedIn Uploader — Design Spec (MVP)

Owner: Maya (Designer)
Date: 2026-03-05

Purpose
- Deliver two UI mocks (Composer + Schedule List) for the LinkedIn post uploader MVP.
- Provide component specs, user flow, wireframes, and design decisions for handoff.

Scope (MVP)
- Composer: connect LinkedIn account, write post, choose template, attach image(s), schedule date/time, preview, save/draft/schedule.
- Schedule List: list of scheduled posts with status, next run time, delivery logs, basic analytics (attempts, success/fail count), actions (edit, cancel, run now), search+filter.

Deliverables & Timeline
- This spec (now).
- 2 high-fidelity mocks: Desktop Composer + Mobile Composer (72h).
- 2 high-fidelity mocks: Schedule List (desktop + mobile) (72h).
- Component library tokens and assets for front-end handoff (72h).

User Flow (core)
1. User connects LinkedIn via OAuth (one account for MVP).
2. User opens Composer: selects template or blank.
3. User composes text, attaches media, sees character count & link preview.
4. User picks schedule (date, time, timezone), or Save Draft.
5. User schedules → entry appears in Schedule List with status "Scheduled".
6. Worker attempts delivery; Schedule List shows logs & analytics; user can retry or cancel.

Composer — Component Specs
- Header: Account badge (LinkedIn icon + name), Connect/Disconnect action.
- Templates rail (left on desktop, collapsible on mobile): template previews (title + preview text) — select to populate editor.
- Editor (center): Rich-text single-field with plain-text focus (LinkedIn text rules). Show live character count and warnings.
  - Max length: show safe limit (we'll confirm exact LinkedIn limit with backend). 
  - Autolink detection + link preview pane (fetched server-side).
- Media uploader: image (up to 4), show thumbnails, drag/drop on desktop, camera/gallery on mobile.
- Schedule panel (right or bottom): date picker, time picker, timezone selector, timezone = user default.
- CTA row: Save Draft, Schedule (primary), Preview.
- Preview drawer/modal: renders LinkedIn post preview (desktop and mobile width).

Schedule List — Component Specs
- Top bar: Search (by text), Filters (status: Draft, Scheduled, Sent, Failed), New Post CTA.
- List view (card for each post): thumbnail, text excerpt, scheduled time (with timezone), status badge, attempts counter, quick actions (Edit, Cancel, View Logs).
- Details panel (side drawer): full post, delivery log (timestamps + worker results), basic analytics: impressions, clicks, likes (if available via API; otherwise show delivered/failed counts), retry button.
- Bulk actions: select multiple -> Cancel or Reschedule.

Wireframes (ASCII)

Composer (Desktop)

[Header: LinkedIn account badge]                 [Preview CTA]
--------------------------------------------------------------
| Templates (left) |          Editor (center)         | Schedule |
| - Template 1     |  [Text input area]              | Date     |
| - Template 2     |  [Attach images] thumbnails     | Time     |
|                  |  [Character count] [Preview]    | Timezone |
--------------------------------------------------------------
[Save Draft] [Schedule]

Schedule List (Desktop)

[Search][Filter:Status]             [New Post]
--------------------------------------------------------------
| Card: Post excerpt                | Status | Time | Attempts |
| [Thumbnail] [Text excerpt]        |Scheduled| 3/10 12:00| 0       |
| Actions: Edit | Cancel | Logs                             |
--------------------------------------------------------------

Key Design Decisions
- Card layout for schedule list: improves scanability and mobile resilience.
- Left templates rail: allows fast reuse without interrupting composition.
- Minimal rich-text: keep editor simple to match LinkedIn formatting; avoid complex styling that LinkedIn won't accept.
- Timezone awareness: schedule times are explicit timezone fields to avoid user confusion.
- Accessibility: keyboard-first editor controls, clear focus states, ARIA labels for media and schedule controls.

Constraints & Questions / Blockers for Design
- Confirm LinkedIn character limits and media constraints (image count, sizes, video support). This affects UI hints and validation.
- Need OAuth redirect URL and any branding restrictions from Legal/Security to show LinkedIn connect flows.
- Analytics availability from LinkedIn API: confirm which metrics are returned for posts (impressions, clicks, likes). If limited, we'll show delivered/failure + placeholders.

Handoff
- Assets & tokens: Inter (font), spacing scale 8px, colors (primary #0A66C2 LinkedIn blue for CTAs), status colors: Scheduled (blue), Sent (green), Failed (red), Draft (gray).
- #ai-frontend Kevin — please review component specs and confirm needed CSS tokens and any technical constraints.
- #ai-product Alex — confirm success metrics to display in UI (impressions/clicks/likes vs delivered/failed).

Next steps (by Maya)
- Produce high-fidelity mocks (desktop + mobile) for Composer + Schedule List within 72h and publish in output/design/.

Files created
- This spec: output/design/linkedin_uploader_design_spec.md

Notes
- I will call out any UX changes required if LinkedIn API responses force constraints (e.g., no video support for MVP).


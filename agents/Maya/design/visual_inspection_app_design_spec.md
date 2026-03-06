# Visual Inspection App — Design Spec (MVP)

Owner: Maya (Design)
Created: 2026-03-06

Purpose
- Deliver wireframes, user flows, component specifications, and design decisions for the Visual Inspection App MVP so frontend (Kevin) can begin implementation.

Assumptions & Constraints
- Primary users: Line Operators (fast-paced), QA Engineers (analysis), Maintenance Techs (action on findings).
- Target platforms: Desktop-first web app (factory control rooms). Responsive to tablet; mobile is low priority for MVP.
- Images/video ingested from edge cameras; backend/API details to be confirmed with Marcus.
- MVP scope: live feed + image ingestion, manual annotation (bounding boxes & defect tags), inspection review, export/reporting of findings, user management minimal.

Open Questions (need Marcus / Alex):
1. Auth & RBAC model: per-user roles? (Operator/QA/Maintenance). I assumed 3 roles.
2. Live feed: WebSocket or periodic polling for frames? Backend decision affects UI buffering.
3. Expected image sizes & frame rate — affects player and thumbnail loading strategy.
4. Annotation persistence model: per-image annotations stored in DB vs sidecar files.

User Flow (MVP)
1. Login → Dashboard (summary of lines + alerts)
2. Select Line → Live Feed / Recent Inspections list
3. Click frame or inspection → Inspection Detail (image or video frame) with Annotation Tools
4. Create/Edit annotation(s) → Save (tag, severity, notes) → Backend ingestion
5. QA reviews → Accept / Reject / Reassign → Export report (CSV/PDF) or send maintenance ticket

Key Screens (wireframes + notes)

1) Dashboard — Summary
- Purpose: quick situational awareness, recent alerts, access to lines.

ASCII Wireframe:
+-------------------------------------------------------------+
| Topbar: Logo | Line selector [Line A v] | User menu [M]       |
+-------------------------------------------------------------+
| Left: Lines list (card per line) | Right: Activity feed     |
| [Line A] [Status: OK / Alert]     | Recent inspections       |
| - Quick actions: View Live, Open Report                         |
+-------------------------------------------------------------+

Notes:
- Cards show last defect count, last inspected timestamp, quick link to live feed.
- Filters: by severity, time range.

2) Live Feed / Line View
- Purpose: monitor the line, freeze frames, jump to recent captures.

ASCII Wireframe:
+-------------------------------------------------------------+
| Topbar: Line: Line A | Camera select [Cam 1 v] | Controls     |
+-------------------------------------------------------------+
| [Live video player large]            | Right rail: Thumbnails  |
| - Play / Pause / Frame step buttons  | - Recent captures list  |
| - Freeze frame (opens Annotation)    | - Filters, search       |
+-------------------------------------------------------------+
| Bottom: Timeline scrubber with markers for detected defects     |
+-------------------------------------------------------------+

Interactions:
- Hover on thumbnail shows quick info; click opens Inspection Detail.
- Freeze frame opens the Annotation Tool overlay (see screen 3).

3) Inspection Detail + Annotation Tool
- Purpose: primary work area for marking defects and adding metadata.

ASCII Wireframe:
+-------------------------------------------------------------+
| Breadcrumb: Dashboard > Line A > Capture 2026-03-06 09:12      |
+-------------------------------------------------------------+
| Left: Image canvas (zoom/pan)         | Right: Metadata panel   |
| - Toolbar: Rect, Polygon, Move, Delete| - Fields: Tag, Severity |
| - Color legend / opacity slider       | - Notes, Attach to ticket|
+-------------------------------------------------------------+
| Bottom: History of annotations (list)  | Save / Cancel / Export  |
+-------------------------------------------------------------+

Component behaviors:
- Annotation tools: bounding box (drag), polygon (multi-point), label selector.
- Snap-to-pixel disabled by default; hold Shift for constrained aspect.
- Undo/Redo stack (Ctrl-Z / Ctrl-Shift-Z).
- When saving, show small toast: "Annotation saved" and optimistic UI update.

4) Reviews & Reports
- Purpose: QA confirms findings and generates reports.

ASCII Wireframe:
+-------------------------------------------------------------+
| Filters bar: Line, Date range, Severity, Status               |
+-------------------------------------------------------------+
| Table: Capture | Time | Tag | Severity | Assignee | Status      |
+-------------------------------------------------------------+
| Actions: Bulk export, Assign to QA, Create maintenance ticket |
+-------------------------------------------------------------+

Design System (MVP subset)
- Layout grid: 12-column, 16px base spacing
- Breakpoints: Desktop (≥1024px), Tablet (≥768px), Mobile (<768px - not primary)
- Colors (provisional):
  - Primary: #0052CC (deep blue)
  - Accent/Severity: Critical: #D32F2F (red), Major: #F57C00 (orange), Minor: #FBC02D (yellow)
  - Background: #F4F6F8, Surface: #FFFFFF
- Typography:
  - Headline: Inter 600, 20-24px
  - Body: Inter 400, 14px
  - Mono for timestamps: Roboto Mono 12px

Component specs (props + accessibility)
- LineCard
  - Props: lineId, name, status, lastDefectsCount, lastInspectedAt
  - Click targets: View Live (primary), Open Report
  - Keyboard: focusable, Enter triggers primary
- VideoPlayer
  - Props: streamUrl, playbackControls (bool), frameRate
  - Accessibility: provide alt text when paused; keyboard shortcuts for play/pause/frame-step
- AnnotationTool
  - Tools: select, bbox, polygon, move, delete
  - Props: image, existingAnnotations
  - Must support keyboard shortcuts and screen-reader friendly metadata panel
- ThumbnailList
  - Virtualized list for performance; lazy-load thumbnails.

Performance & UX considerations
- Virtualize lists (thumbnails, reports) to handle large datasets.
- Progressive image loading: low-res placeholder -> high-res on demand.
- Avoid blocking UI on save: optimistic updates + background sync.

Acceptance Criteria for Frontend
- Implement screens described above with responsive behavior and component APIs matching specs.
- All annotation interactions work with undo/redo and persist to backend API (to be defined by Marcus).
- Provide unit tests for critical components (LineCard, VideoPlayer, AnnotationTool).
- Implement color tokens and typography tokens per design system values.

Deliverables (attached)
- This design spec: output/design/visual_inspection_app_design_spec.md
- Wireframes (ASCII) embedded above

Next steps / Handoff
- Frontend (Kevin): implement components and screens. See "Next Steps" in the Slack handoff.
- Backend (Marcus): confirm API for fetching streams/thumbnails, annotation save endpoints, pagination strategy, and expected image sizes.

Design decisions rationale (one-line each)
- Desktop-first: primary users are control-room staff who use desktop screens.
- Card list + right activity rail on dashboard: balances quick scanning with actionable items.
- Separate Annotation metadata panel: keeps canvas uncluttered and improves accessibility.

Notes for implementation
- Use canvas/SVG for annotation layer to allow high-performance drawing.
- Keep annotation geometry normalized to image coordinates (0..1) so backend storage is resolution-agnostic.
- Provide hooks/events: onAnnotationSave, onAnnotationSelect for integration tests.

Open tasks for Kevin (frontend)
- Confirm choice of annotation library (fabric.js, Konva, or build custom) — I prefer Konva for React integration.
- Implement tokenized color & typography system.
- Build reusable component library for LineCard, Thumbnail, VideoPlayer, AnnotationTool.

Contact
- Maya (Design) — available for design reviews and implementation QA.

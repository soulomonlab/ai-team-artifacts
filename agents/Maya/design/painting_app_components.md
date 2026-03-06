# Painting App — Design Spec & Component Library

Summary
- Confirmed decisions: raster-first (HTML5 Canvas + WebGL), client-side undo/redo op-stack, autosave every 10s to S3, stateless APIs, performance target: interaction <100ms.
- Open question / flag: offline-first support is NOT specified. If required, it changes persistence and sync design (see "Offline & Sync implications").
- Deliverables in this file: user flows, ASCII wireframes, component specs, accessibility & performance notes, design decisions.

User personas & context
- Primary user: hobbyist or professional creating digital paintings in desktop browsers. Secondary: tablet users with stylus.
- Usage context: medium-length sessions (5–120 minutes), expectation of low input latency, frequent undo/redo, occasional exports.

User flows (high level)
1. New painting
   - User clicks New → choose canvas size/resolution → canvas initialized locally (op-stack empty) → start painting.
2. Resume painting (autosave)
   - App loads last autosave for session ID / user from S3 (if available) → rehydrate op-stack or raster snapshot → user continues.
3. Save / Export
   - Manual Save/Export → user selects format (PNG/JPEG/PSD) → client-side export using canvas.toBlob / offscreen rendering → upload to S3 or prompt download.

Wireframes (ASCII)
- Desktop layout (primary):

+-------------------------------------------------------------+
| Topbar: Logo | File | Edit | Export | Settings                |
+-------------------------------------------------------------+
| Toolbar (left) |                 Canvas area               |
| [Brushs]       |                                       |R  |
| [Eraser]       |               CANVAS (WebGL)           |i  |
| [Fill]         |                                       |g  |
| [Color swatch] |                                       |h  |
+-------------------------------------------------------------+
| Layers panel (right) | History / Undo-Redo | Bottom status: Zoom, Autosave status |
+-------------------------------------------------------------+

- Mobile / Tablet: condense toolbar into bottom sheet; canvas full-bleed; floating quick actions (undo, brush size).

Component specs
(Spacing base = 8px, container gap = 16px)

1) CanvasContainer
- Purpose: host WebGL/2D canvas and overlay UI (selection boxes, cursor preview).
- Behavior: responsive full-area, maintains aspect ratio option, supports devicePixelRatio scaling.
- Notes: use <canvas> for rendering; overlays (selection bounding boxes, tool cursors) are DOM layers positioned absolute.

2) ToolBar (left, collapsible)
- Items: Move, Brush, Eraser, Fill, Smudge, Color Picker, Eyedropper, Text, Shapes
- Width: 56px collapsed, 220px expanded
- States: active, hover, disabled
- Interaction: keyboard shortcuts, long-press for sub-tools (mobile)

3) BrushPanel (drawer)
- Controls: size slider (0–200px), hardness, opacity, flow, spacing, custom brush import
- Live preview: 120x80 px preview canvas
- Defaults: 8px size, hardness 80%, opacity 100%
- Keyboard shortcuts: [ , ] to decrease/increase size

4) ColorPicker
- Contains: swatches, color wheel, hex input, eyedropper
- Swatch size: 28px square
- Accessibility: supports keyboard input for hex and presets

5) LayersPanel
- Items: thumbnail (64x64), layer name, opacity slider, visibility toggle, lock toggle, blend mode dropdown
- Reorder: drag & drop
- Context menu: duplicate, merge down, delete

6) History / Undo-Redo
- Primary UI: undo/redo buttons in topbar + history dropdown (stack list with timestamps)
- Behavior: show last N operations (configurable, default 50). For performance, store op-stack as compact ops; optionally snapshot every N ops.

7) Autosave Indicator
- Position: bottom-right status bar
- States: Idle, Saving (spinner), Saved (timestamp), Failed (error with retry)
- Autosave cadence: every 10s (as specified) but debounce when user is actively drawing (save 2s after inactivity)

8) Export Modal
- Options: Export as PNG (flattened), JPEG (quality slider), PSD (layers)
- Export resolution multiplier: 1x/2x/3x

9) Settings Modal
- Options: Canvas defaults, Autosave toggle & interval, Storage target (S3 path), Undo depth, Offline mode

Design decisions & rationale
- Raster-first with WebGL: provides best rendering performance for brushes and large canvases. Overlay DOM for UI keeps accessibility manageable.
- Client-side op-stack: gives instant undo/redo; store compact ops + periodic raster snapshot to limit memory and speed rehydration.
- Autosave every 10s to S3: use optimistic local saves with background uploads to S3. Show indicator and retry logic.
- Keep UI chrome minimal: prioritize large canvas area, collapse panels by default.

Offline & Sync implications (flag)
- If offline-first required: implement IndexedDB local storage for snapshots + op-stack, plus background sync queue to upload to S3 when online.
- Conflict model needed: last-writer-wins is simplest but may surprise users. Better: versioned saves + UI conflict resolution for divergent edits.
- Complexity: offline-first increases scope significantly (merge algorithms, storage, increased QA). Please confirm requirement.

Performance notes (must meet <100ms interaction)
- Use requestAnimationFrame for brush strokes; batch ops; use OffscreenCanvas and transfer to WebGL where available.
- Keep DOM minimal; do not re-render React tree per pointermove.
- Limit JS work on main thread during painting; use Web Workers for brush computation if needed.
- Use devicePixelRatio scaling carefully to balance quality vs memory.

Accessibility
- Keyboard shortcuts for common actions (B=brush, E=eraser, Z=undo, Y=redo)
- ARIA labels for panels and controls
- Color contrast: ensure UI meets AA for controls

Assets & Figma
- I'll create a Figma file and upload component frames + tokens. Placeholder: Figma file will be shared in the next update.

Open questions / decisions needed from Product / Tech
- Confirm offline-first requirement (yes/no). If yes, prioritize IndexedDB + sync design.
- PSD export: must server-side flattening be supported or can client generate multi-layer PSD? (client PSD libs have limits)
- Max canvas size target (px) — affects memory and tiling strategy.

Next steps
- Create Figma with components & tokens (in progress).
- Hand off this spec to #ai-frontend (Kevin) for implementation estimates and feasibility checks.

Design owner: Maya (UX/UI)
File: output/design/painting_app_components.md

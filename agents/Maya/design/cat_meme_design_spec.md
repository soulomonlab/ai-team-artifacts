# Cat Meme App — Design Spec (MVP)

## Summary
Deliverables created for #114 (P1): 3 responsive wireframes (mobile/tablet/desktop), UI kit for editor controls, and 10 vector cat templates (SVG) placed under output/design/templates/. These assets follow PRD constraints (React + Konva frontend; Lambda + S3 backend; single-region + CDN; performance targets).

## Key decisions (recorded)
- Canvas tech: Konva on React (from PRD) — design assumes immediate canvas manipulations + layer model.
- Templates: deliver as SVG vectors (reversible to PNG). Frontend should rasterize/export to PNG via canvas for performance and size control.
- Editor layout: left vertical toolbar (desktop/tablet) → bottom toolbar (mobile). Rationale: preserves canvas center, easier touch reach on mobile.
- Default canvas size: 1024×1024 px (export cap ≤1MP). Exports should offer 512/1024 options; ensure retina scaling handled client-side.
- Performance constraints: critical interactions (tool select, drag, text edit) must be under 1500ms on 3G; templates lazy-load; use thumbnails + CDN.

## User flows (high-level)
1. Open app → choose template or blank → editor loads selected template on canvas.
2. Edit: move/scale/rotate stickers (templates), add text layers, change font/color, undo/redo, save to S3, export PNG.
3. Share/export: quick export modal with size presets and download button.

## Acceptance criteria (design)
- Wireframes: clear layouts for mobile/tablet/desktop; toolbar/components match UI kit.
- UI kit: tokens (colors, typography), component states, spacing, interaction specs.
- Templates: 10 SVGs with sensible names/tags and thumbnail references.

## Files created
- output/design/cat_meme_design_spec.md (this file)
- output/design/ui_kit_editor_controls.md
- output/design/cat_templates_manifest.md
- output/design/templates/template01.svg ... template10.svg

## Notes for frontend (Kevin)
- Use Konva layer model: background template layer (immutable by default), sticker layer, text layer, UI overlay.
- Templates provided as SVG; load as images onto Konva or parse into nodes. Prefer rasterizing to reduce runtime DOM complexity.
- Lazy-load template thumbnails; load full SVG only when user selects.


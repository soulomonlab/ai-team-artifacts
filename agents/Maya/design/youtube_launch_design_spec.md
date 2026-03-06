YouTube Launch — Design Spec

Purpose
- Deliver visual assets, rules, and implementation-ready specs for the YouTube launch hero, thumbnail, and banner A/B tests.
- Provide accessibility guidance and export requirements so frontend can implement quickly and consistently.

Deliverables (this file)
- Figma master file (add link here): https://www.figma.com/file/REPLACE_WITH_FIGMA_LINK
- Export instructions & asset sizes (below)
- Component specs, copy & thumbnail rules
- Accessibility notes
- Wireframes (desktop + mobile)
- Implementation notes for #ai-frontend and coordination note for #ai-backend

Primary audience
- Frontend engineers (Kevin)
- Backend (Marcus) for analytics hooks
- QA for visual checks

Event & tracking context (per Growth brief)
- Events to instrument: video_impression, video_click, youtube_subscribe_click, video_share, upload_checklist_completed
- UTM capture: utm_source, utm_medium, utm_campaign, utm_term, utm_content
- Frontend must include data attributes on interactive elements (see Implementation notes)

Thumbnail rules
- Headline: max 3–4 words. Keep to a single-line when possible.
- Legibility: target min readable size = 40–50px at 1280x720 export. Use bold weights for short words.
- Safe area: keep important content at least 10% inset from each edge (no text within 10% margin).
- Text coverage: text must not cover more than 30% of visible area.
- Contrast: text over image must meet AA (4.5:1) for body-size text; for large/hero text minimum 3:1.
- Branding: place small logo in top-left (max 8% width). Keep it subtle.
- CTA/Badge: if including a play-badge or subscribe badge, keep it bottom-right, 8% inset.
- Visual treatments: subtle drop shadow on text (blur 8–12px, rgba(0,0,0,0.45)) and 3–6px outline for white text against light imagery.

Thumbnail file naming & format
- Naming: yt_{videoId}_thumb_v{variant}_{w}x{h}.jpg
- Formats: JPEG for photographic thumbnails (quality 80), PNG for thumbnails requiring transparency.
- Required exports (all from Figma at 1x and 2x retina):
  - Primary YouTube thumbnail: 1280x720 (1x) and 2560x1440 (2x)
  - Small preview thumbnail: 480x270
  - Social share crop (square): 1200x1200
  - Mobile hero thumbnail (in-UI): 640x360

Hero / Banner assets
- Desktop hero (full-width): 1200x400 (also provide a 1600x533 for larger screens)
- Mobile hero: 640x360
- Thumbnail slot for hero: 320x180 (plus 2x retina)
- Provide 3 thumbnail variants per video for A/B testing (Variant A: text-left; Variant B: text-bottom overlay; Variant C: no-text image)

Component specs
1) Thumbnail component
- Aspect ratio: 16:9 fixed
- Overlay: optional semi-transparent gradient bottom (rgba(0,0,0,0.28)) to improve legibility
- Data attributes (for instrumentation):
  - data-event="video_impression" (on image when entering viewport)
  - data-event="video_click" (on click/press) and data-video-id="{videoId}"
  - data-utm attributes: data-utm-source, data-utm-medium, data-utm-campaign, data-utm-term, data-utm-content

2) Banner/Hero component
- Layout: Desktop two-column (thumb left, content right). Mobile stacked (thumb top, content bottom).
- CTA button: primary color, min target size 44x44px, label examples: "Watch", "Subscribe"
- A/B variants: (A) CTA-first (CTA prominent), (B) Thumbnail-first (visual-first). Track impressions and clicks per variant with data-ab-variant="A" / "B".

Wireframes (ASCII)
- Desktop
  ------------------------------------------------
  | [ THUMB 16:9 ]  |  Headline (H2)             |
  |                |  Description (1 line)      |
  |                |  [ CTA ]   [Secondary link]|
  ------------------------------------------------

- Mobile
  -------------------------
  | [ THUMB 16:9 ]        |
  | Headline (center)     |
  | [ CTA ]               |
  -------------------------

Accessibility
- Contrast: meet WCAG AA for text. Use checked color tokens.
- Alt text: every thumbnail image must include alt text: "Thumbnail: {videoTitle} — {short purpose}".
- Keyboard: thumbnail tiles and CTAs must be focusable (tabindex=0). Provide visible focus ring (2px solid #005fcc or 2px box-shadow).
- Motion: avoid autoplay animations. If using hover transitions, provide a non-motion fallback.

Typography & color
- Brand font: Inter (or system sans if not available). Headline weight: 700. Body: 400.
- Color tokens (use design system tokens):
  - Primary: #005FCC
  - Accent: #FFB400
  - Dark text: #111827
  - Muted: #6B7280

Decisions & rationale
- Thumbnail: short text + strong contrast maximizes CTR on small previews.
- Safe area & text cap reduces localization/layout issues and improves legibility on small devices.
- Provide 3 variants to A/B quickly converge on highest CTR while limiting creatives cost.

Implementation notes for frontend (Kevin)
- Use data attributes listed above for instrumentation. Coordinate with Marcus to confirm server event ingestion endpoints exist before final analytics wiring.
- Provide Storybook stories for Thumbnail and Hero with three thumbnail variants and A/B flag knobs.
- Exports: ask Design for PNG/JPG assets or export directly from Figma. File path convention: /assets/youtube/{videoId}/
- Accessibility: ensure alt text and focus states are implemented.

QA checklist (deliverable-ready)
- Visual match to Figma artboard (pixel tolerance 2px)
- All images load with correct srcset for retina
- Data attributes present and firing events (with dev console or network inspector)
- Contrast checks pass

Next steps (short)
- I will upload Figma master and export assets. (Figma link placeholder above.)
- #ai-frontend (Kevin): implement hero/banner slots, Storybook components, A/B hooks per spec.
- Recommend #ai-backend (Marcus) implement event ingestion endpoints + UTM capture before frontend wiring.

Files created
- This spec: output/design/youtube_launch_design_spec.md

Notes
- If Marcus needs exact data payloads for events I can add sample payloads — say so and I’ll add them to this spec.

Design owner: Maya (UX/UI)

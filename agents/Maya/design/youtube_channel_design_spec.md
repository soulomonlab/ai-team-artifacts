YouTube Channel Design Assets — Spec + Export Instructions

Overview
- Deliverables (task #103, P1):
  1) Banner template (Figma source + exports)
  2) Avatar (profile photo) assets
  3) Thumbnail template(s) with export presets
  4) Accessibility notes + thumbnail text rules

Files produced:
- output/design/youtube_channel_design_spec.md (this file)

Design decisions (summary)
- Thumbnail-first approach: thumbnails drive CTR on YouTube; templates prioritize clear focal point + bold short text to improve click-through.
- Banner responsive safe-area: many users view on mobile; ensure critical info sits inside 1546x423 safe area of 2560x1440 master artboard.
- Avatar: circular crop; keep logo/face centered with enough breathing room for small sizes.
- Accessibility: WCAG-focused contrast for thumbnail text (>=4.5:1 for body-sized text; >=3:1 for large). Use bold sans-serif fonts at readable sizes.

Figma source
- Figma file: "YouTube Channel — ChannelAssets (Maya)"
- Page structure: /Banner, /Avatar, /Thumbnails/Templates, /Exports
- Figma components: Thumbnail Card, CTA Badge, Safe Area Guides
- Export workflow: produce PNG/JPG per spec below. Add 2x (retina) export variants where listed.

Banner (master)
- Master size: 2560 x 1440 px (export PNG)
- Safe area (KEEP ALL CRITICAL CONTENT HERE): centered 1546 x 423 px
- Visible on desktop: 2560 x 423 px; on TV: full 2560 x 1440; on mobile: center 1546 x 423
- Recommended exports:
  - banner_master.png — 2560x1440 (PNG)
  - banner_desktop.jpg — 2560x423 (JPG, 80% quality)
  - banner_mobile.jpg — 1546x423 (JPG, 80% quality)
- Guidelines: place channel title / social handle within safe area; avoid small text near edges; include subtle brand gradient for recognizability.

Avatar (profile)
- Master size: 800 x 800 px (square)
- Exports:
  - avatar_800.png — 800x800 (PNG, transparent allowed)
  - avatar_200.png — 200x200 (PNG)
  - avatar_98.png — 98x98 (PNG) — used in-site small profile
- Guideline: center logo/face; leave 10% padding around subject; export as PNG for sharpness.

Thumbnail template(s)
- Primary spec: 1280 x 720 px (16:9) — JPG (preferred) or PNG
- Exports:
  - thumb_1280.jpg — 1280x720 (JPG, 85% quality)
  - thumb_1280@2x.jpg — 2560x1440 (retina)
  - thumb_640.jpg — 640x360 (fallback)
- Mobile crop preview: supply a 4:3 center crop preview in CMS to ensure main subject/text remains visible on phones.

Thumbnail composition rules (text rules)
1) Short headline only: 2–4 words recommended; max 6 words in exceptional cases.
2) Use strong contrast: text color should meet at least 4.5:1 contrast against background when <24px; large text (>=24px) should meet 3:1.
3) Title placement: bottom-left or bottom-third; leave 10% margin from edges.
4) Safe area: keep main subject/face centered in middle 60% horizontally and 70% vertically.
5) No more than 2 font sizes in thumbnail. Prefer bold weight for headline.
6) Avoid full-sentence overlays. Prefer punchy verbs/nouns.
7) Branding: include small channel logo badge (40–80px width) in top-left or top-right; ensure it does not occlude subject.

Typography
- Primary headline font: Inter / Montserrat (bold) for readability.
- Secondary: Inter Regular for subcopy.
- Suggested sizes (for 1280x720): headline 72–96px; subcopy 36–48px depending on length.

Color & Contrast
- Primary brand color: #FF5A5F (example) — use for CTA badges
- Accent: #00A3FF
- Neutral dark: #111827 (text)
- Use white (#FFFFFF) or dark overlay (rgba(0,0,0,0.45)) behind text if background contrast is low.

Accessibility notes
- Alt text: always provide descriptive alt text for thumbnails and banner during upload (1-line summary of video content + speaker name if applicable).
- Color contrast checks: run automated check in build to ensure text contrast meets rules above.
- Avoid small decorative text as only source of meaning.

Export and naming convention (example)
- channel_banner_master_2560x1440.png
- channel_banner_mobile_1546x423.jpg
- channel_avatar_800.png
- thumbnail_{video-slug}_1280.jpg
- thumbnail_{video-slug}_1280@2x.jpg

Upload workflow requirements (for frontend/UX handoff)
- Accept file types: JPG, PNG. Max file size: 8 MB (suggest compress during upload to <=2MB for thumbnails). Validate dimensions and ratios.
- Provide instant preview with safe-area overlay toggles (banner safe-area; thumbnail center safe crop; circular avatar crop preview).
- Auto-generate 2x retina export and smaller fallback versions after upload.
- Show contrast warnings if text overlay in uploaded thumbnail fails contrast rules.
- Required metadata fields on upload: title, alt text, thumbnail role (primary/secondary), thumbnail text override (for QA).

Implementation notes (for engineering)
- Provide both PNG and JPG outputs; prefer JPG for thumbnails to reduce bandwidth.
- Provide a client-side preview that simulates YouTube display sizes (desktop, mobile, TV)

Wireframes (ASCII)
- Thumbnail template (1280x720)
  +---------------------------------------------------------------+
  | [Hero image: subject on left or center]                        |
  |                                                               |
  |                        HEADLINE (bottom-left)                 |
  |  [small channel badge]                                        |
  +---------------------------------------------------------------+

- Banner safe area
  +---------------------------------------------------------------+
  |<-- left/right cropping →>                                     |
  |  [2560x1440 master]                                           |
  |     +-----------------------------------------------+         |
  |     | 1546 x 423 px SAFE AREA (centered)             |         |
  |     |  [Channel title / 1-line CTA / Social icons]   |         |
  |     +-----------------------------------------------+         |
  +---------------------------------------------------------------+

Deliverables to handoff
- Figma file (see above) — I'll upload once PRD assets approved
- Spec file (this): output/design/youtube_channel_design_spec.md
- Preview templates (placed in Figma / exports folder) — filenames per naming convention

Open decisions / questions for product (Alex)
- Should thumbnails include episode numbers? (Pros: series clarity; Cons: clutter and may reduce clickability)
- Confirm brand primary color hex to finalise templates

Next: handoff to frontend to implement upload + preview flow and to export images via build pipeline.

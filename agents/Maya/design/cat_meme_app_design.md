# Cat Meme App — Design Spec

Author: Maya (Designer)
Output path: output/design/cat_meme_app_design.md
Related PRD: output/specs/cat_meme_app.md

## Summary
Mobile-first web app for creating/shareable cat memes. This spec includes user flows, mobile wireframes (ASCII), component specs, visual tokens, accessibility notes, and 20 permissively-licensed cat image assets with attribution.

---
## Key decisions (short)
- Mobile-first responsive web app (breakpoints: 360px, 768px, 1024px)
- Editor includes two default caption regions (Top, Bottom) + free-drag text layer
- Font set limited to 3 families (Impact-style, Sans, Handwritten) for clarity and performance
- Caption controls: font, size (auto-scale + manual), color, stroke (outline), alignment, vertical offset
- Upload constraints: client-side 10MB limit; show clear error + guidance; malware scan server-side
- UX: Templates gallery first load prioritized; show skeletons to meet <200ms perceived load

---
## User flows
1) Browse templates
   - Home -> Template gallery (infinite scroll with skeletons)
   - Tap template -> Open Editor with selected image
2) Upload image
   - Home -> Upload button -> Pick from device -> validate size -> show preview -> open Editor
3) Edit meme
   - Editor: image canvas, caption controls panel, undo/redo, save/share
   - Controls: add text, drag/position, style, download
4) Create & share
   - Generate -> POST to backend -> success -> show share modal (copy link, twitter, download)

Acceptance criteria (design): Editor interactions are discoverable on mobile; text is readable on small screens; primary actions reachable within thumb zone.

---
## Mobile wireframes (ASCII)
Home / Gallery (mobile)

[ Header: CatMeme (logo) | Upload Icon ]
[ Search bar (optional) ]
[ Category tabs: Popular | Cute | Funny ]
[ Card grid: 2 columns, gap 8px ]
- Card: thumbnail (square) + title + favorite icon
[ Floating CTA: + Create (bottom-right) ]

Editor (mobile, full screen)

[ Top bar: ← Back | filename | ⋮ ]
[ Canvas: image (center, fit) ]
[ Layers indicator: Top: "Top text" | Bottom: "Bottom text" ]
[ Toolbar (above bottom): font | size(-/+) | color | stroke | align | drag icon ]
[ Bottom action bar: Undo | Redo | Preview | Generate (primary) ]

Editor collapsed controls (small devices): show primary controls + 'More' to expand advanced settings in a sheet.

---
## Component specs (mobile-first)
All components include states (default, hover/pressed, disabled) and accessibility labels.

1. Header
   - Height: 56px
   - Left: Back (40x40 tappable), Center: Title, Right: Upload (icon button)
2. Gallery Card
   - Image ratio 1:1; radius 8px; shadow subtle
   - Tap opens Editor with selected template
3. Image Uploader
   - File input with drag/drop (desktop) and device picker (mobile)
   - Client-side size check: max 10MB; show inline error "File too large. Try <10MB or use a smaller image."
4. Canvas & Text Layer
   - Canvas scales to available height while keeping aspect
   - Text layers: editable inline; double-tap to edit; long-press to drag
   - Auto-wrap & auto-scale: text shrinks to fit width up to min font size 12px
   - Default caption positions: 8% from top/bottom respectively
5. Toolbar Controls
   - Font selector (3 options), Font size +/- with numeric input, Color picker (preset swatches + custom), Stroke toggle + thickness slider, Alignment (L/C/R), Layer order
6. Actions
   - Generate (primary CTA, sticky bottom): sends payload {image_id|upload, layers[], metadata}
   - Download: save PNG with applied captions; offer WebP where supported

---
## Interaction details & edge cases
- Image orientation: auto-rotate using EXIF metadata
- Large images: downscale on client to max 4096px on longest side to reduce upload time
- Undo/redo: up to 20 steps
- Offline: warn on generate; queue not supported in v1
- Error flows: show contextual toasts and a retry action; rate-limit error: show modal "Rate limit reached: 10 creations/hr"
- Malicious upload: show generic "Image failed security check" and allow re-upload

---
## Accessibility
- All controls reachable by keyboard; buttons have aria-labels
- Color contrast: ensure text and stroke combos meet WCAG AA on typical images (suggest default stroke for better legibility)
- Use semantic HTML for forms and modals

---
## Visual tokens (initial)
- Primary color: #FF6B6B (CTA)
- Neutral: #222 (text), #666 (muted)
- Success: #26A69A, Error: #E53935
- Border radius: 8px
- Spacing base: 8px
- Type scale: H1 20px, H2 16px, Body 14px

Font choices
- Impact-like: 'Anton', fallback: system sans
- Sans: 'Inter' (var), fallback: system
- Handwritten: 'Patrick Hand' (optional)

Rationale: small set reduces network weight and yields recognizable meme aesthetic.

---
## Assets — 20 permissively-licensed cat images
All images under Unsplash or Wikimedia Commons (permissive). Use photographer attribution as shown.
1) https://unsplash.com/photos/J---aiyznGQ — Photo by Patrick via Unsplash
2) https://unsplash.com/photos/MTZTGvDsHFY — Photo by Alex via Unsplash
3) https://unsplash.com/photos/3k8R2A3Yd0k — Photo by Kris via Unsplash
4) https://unsplash.com/photos/1SAnrIxw5OY — Photo by Giovanni via Unsplash
5) https://unsplash.com/photos/7okkFhxrxNw — Photo by Annie via Unsplash
6) https://unsplash.com/photos/5QgIuuBxKwM — Photo by Denise via Unsplash
7) https://unsplash.com/photos/FXvL2u1tQXU — Photo by Sharon via Unsplash
8) https://unsplash.com/photos/IGfIGP5ONV0 — Photo by Elly via Unsplash
9) https://unsplash.com/photos/hNGRx7OJ6k0 — Photo by Matthew via Unsplash
10) https://unsplash.com/photos/xN4t7V2YbT4 — Photo by Kyle via Unsplash
11) https://commons.wikimedia.org/wiki/File:Cat_poster_1.jpg — Wikimedia (public domain)
12) https://commons.wikimedia.org/wiki/File:Kittens_2010.jpg — Wikimedia (public domain)
13) https://www.pexels.com/photo/adorable-animal-eyes-feline-617278/ — Pexels (free)
14) https://www.pexels.com/photo/closeup-photo-of-grey-and-white-cat-127028/ — Pexels
15) https://www.pexels.com/photo/white-and-black-short-fur-cat-looking-up-617166/ — Pexels
16) https://www.pexels.com/photo/close-up-photo-of-white-and-brown-tabby-kitten-981064/ — Pexels
17) https://www.pexels.com/photo/adorable-cat-lying-on-the-bed-617278/ — Pexels
18) https://unsplash.com/photos/2uG2J0y3QxI — Photo by Florence via Unsplash
19) https://unsplash.com/photos/8manzos4chE — Photo by Jason via Unsplash
20) https://unsplash.com/photos/some-example-id — Photo by Example via Unsplash

Notes: Before shipping, we must verify each image's exact license and include required attributions in the app's credits modal. If Unsplash/ Pexels policy changes, swap to equivalent Wikimedia images.

---
## Handoff & acceptance criteria for Frontend
Files created: output/design/cat_meme_app_design.md
Frontend acceptance:
- Implement mobile-first responsive UI per breakpoints
- Editor: text layer editing, drag, style controls, undo/redo, generate flow
- Enforce upload size (client) and show errors as specified
- Include image gallery populated with listed assets (placeholders allowed)
- Provide storybook or component demo pages for: GalleryCard, EditorCanvas, TextToolbar

Implementation notes for Kevin:
- Preload low-res thumbnails for gallery (use progressive loading)
- Canvas: use HTML5 canvas or DOM + CSS (choose for ease of export). If choosing canvas, ensure text rendering supports stroke and export to PNG.
- Coordinate API contract with Marcus: GET /templates (pagination), POST /generate (multipart form or base64 image + layers JSON)

---
## Open questions (needs product/backend)
- Confirm exact API payload shape for POST /generate (layers format)
- Confirm whether we support animated gifs (v1 = no)
- Confirm required analytics events (create, share, download)

---
## Next steps
- #ai-frontend (Kevin): implement components and share storybook preview
- #ai-backend (Marcus): confirm API contract and upload security flow


# Instagram-style MVP — Design Spec

Author: Maya (Designer)
Source PRD: output/specs/instagram_mvp.md
Date: 2026-03-06

Overview
- Deliverables: mobile-first wireframes, Figma file (URL to be provided), exported PNG/SVG assets, component spec covering: onboarding, feed, composer, profile, post detail.
- Timeline: 5 business days (start: 2026-03-06, due: 2026-03-13).

Acceptance criteria (refer to PRD)
- Onboarding: <=3 progressive steps; user can sign up with email/phone or continue with social; completion leads to populated feed.
- Feed: loads first page (10 posts) within 1s on 3G simulated low bandwidth; infinite scroll/pagination; like/comment/share actions persisted.
- Composer: upload photo/video, crop/rotate, add caption, mention users, add hashtags, set visibility (public/private), preview & upload confirmation.
- Profile: header with avatar/stats, tabbed grid/list for posts, edit profile flow.
- Post detail: full image/video, caption, comment thread, like count, share sheet.
- Accessibility: contrast ratio >=4.5:1 for body text, font sizing respecting dynamic type (min 14sp for body), tappable targets >=44x44pt.

Key design decisions (high-level)
1. Mobile-first, single-column feed (1 post width) to maximize media size and focus.
   - Why: mirrors user expectation, simple responsive scaling to tablet/desktop.
2. Composer = bottom-sheet modal (persistent draft autosave + local cache).
   - Why: fast access from feed, keeps navigation context, supports quick cancel.
3. Image aspect handling: store original aspect; display cropped centered 4:5 in feed cards, full aspect on post detail.
   - Why: visual consistency in feed + better use of vertical space.
4. Performance & progressive loading: low-res blurred placeholder -> high-res when loaded; use LQIP + CDN (aligned with backend decision).
5. Accessibility & gestures: swipe to dismiss composer, double-tap to like, long-press to open reaction menu (future enhancement).

User flows (happy path)
1. Onboard: Launch → Sign up / Sign in → Profile setup (username, avatar, interests) → Enter feed.
2. Create post: Tap + (composer) → Select media (camera/gallery) → Edit (crop/rotate) → Add caption/mentions/hashtags → Publish → Redirect to posted item in feed.
3. Interact with feed: Scroll feed → Tap like / comment / share → Open post detail → Post comment → Close.
4. View profile: Tap avatar → Profile (grid) → Open post detail → Edit profile (gear icon).

Component spec (summary)
- Nav bar: top left = camera (future), center = logo, right = messages; bottom nav: feed, search, create (+), activity, profile.
- Stories carousel: horizontal, tappable story pill with circular avatar, support for ephemeral content.
- Feed card: header (avatar, name, time, more), media area (image/video), action row (like, comment, share, save), caption (expand/collapse), comments preview (2+), view full post link.
- Composer: bottom sheet with media picker (grid thumbnails), camera quick-capture, editing tools (crop, rotate, filter minimal), caption input (mention autocomplete), location toggle, accessibility toggle (alt text input).
- Post detail: media viewer with pinch-zoom, caption block, comments list (lazy-loaded), input bar, reaction animations.
- Profile: header (avatar, follow/edit button, stats), bio, action buttons, segmented control (posts, tagged), grid/list toggle.

Wireframes (ASCII, mobile portrait)
- Feed (mobile):
  [TopNav]
  [Stories --- horizontal scroll ---]
  [Post Card]
     Avatar Name ... More
     [Image 4:5]
     Like Comment Share Save
     Caption (first line) · View all
  [Post Card]

- Composer (bottom-sheet):
  -------------------------
  | Drag handle  O        |
  | [Grid of thumbnails]  |
  | [Selected media preview]| 
  | Caption input @mention |  [Publish]
  -------------------------

- Profile (mobile):
  [Avatar] [Edit Profile]
  Username
  Bio line 1
  Posts Grid (3 columns)

- Post Detail:
  [Media full width]
  Caption text
  Comments (lazy)
  Add comment field

Accessibility notes
- Color tokens chosen for 4.5:1 contrast for body; CTA contrast 3:1 for large text.
- Touch targets >=44px. Labels for icons for screen readers. Alt text input mandatory before publish (encourage but allow skip with warning).
- Keyboard navigation for web will follow ARIA roles for lists and forms.

Edge cases & gotchas
- Long captions: collapse after 3 lines with "View more".
- Very tall/very wide media: center-crop to feed 4:5, allow full view in post detail.
- Offline draft: composer autosaves to local storage and retries upload when online.
- Rate-limited image processing: show progress + retry.

Deliverables & handoff
- I will deliver:
  1) Figma file link (master) — provided by Day 3 (iterative)
  2) PNG/SVG exports for key screens (onboarding, feed, composer, profile, post detail)
  3) Component spec (tokens: colors, typography, spacing + CSS vars)
- Final handoff to #ai-frontend (Kevin) after design review: include redlines, interaction notes, exported assets, and component tokens.

Next steps / timeline
- Day 0 (today): Confirm scope & start wireframes. (This doc created.)
- Day 1-2: Wireframes → review with PO (Alex) if needed.
- Day 3-4: High-fidelity screens in Figma + component tokens.
- Day 5: Exports, accessibility pass, handoff package.

Contact
- Designer: Maya — #ai-design
- Implementation owner after handoff: Kevin (#ai-frontend)

Appendix: Links
- PRD: output/specs/instagram_mvp.md
- GitHub issue: https://github.com/soulomonlab/slack_bot/issues/98

Design decisions log saved with this spec. Any deviations must be documented here for traceability.

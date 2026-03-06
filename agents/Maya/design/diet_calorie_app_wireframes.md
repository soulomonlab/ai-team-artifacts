Diet Calorie App (v1) — Mobile-first Wireframes & Design Spec

Summary
- Mobile-first design for MVP: manual food search + recent + favorites.
- Focus: fast search, clear food card hierarchy, easy add-to-diary flow.
- Barcode scanner deferred to v1.1.

User flow (primary)
1. Launch -> Auth (Email/OAuth)
2. Home (Daily summary + Add button) -> Search
3. Search results -> Select food -> Food detail -> Adjust serving -> Add to diary
4. View Recent / Favorites from Home or Search

Key screens (mobile)
- Auth: Email sign-in / OAuth buttons
- Home: daily calories, bottom navigation, prominent "+" Add button
- Search: search bar, recent queries, suggestions, list of food cards
- Food Detail Modal: photo, brand, calories per serving, macros, serving selector, Add CTA
- Diary Entry Confirmation (toast + quick edit) 
- Favorites screen

Component specs
- Layout
  - 375pt width baseline (iPhone 8 / common mobile)
  - 16pt outer padding, 12pt between vertical stacks
- Bottom nav
  - 5 items: Home, Search, Add, Favorites, Profile
  - Floating circular primary Add (48px) centered, elevated shadow
- Search bar
  - Full-width, rounded (20px radius), placeholder "Search food or brand"
  - Typeahead list below with up to 5 suggestions
- Food Card
  - Height ~84px; horizontal card with thumbnail (64x64), title, brand, calories, micro-info (protein/fat/carbs)
  - Tap anywhere to open Food Detail
- Food Detail
  - Top photo (optional), name, brand, large calorie count (bold), serving size dropdown, quantity stepper, Add button (primary)
- Colors & typography (tokens)
  - Primary: #0A84FF (blue)
  - Surface: #FFFFFF; Muted text: #6B7280; Strong text: #111827
  - Body: Inter 16/24, H1: 20/28 semibold
- Accessibility
  - Contrast ratios >= 4.5:1 for text on backgrounds
  - Touchable targets >= 44x44pt

Wireframes (ASCII)
- Home
  ---------------------------------
  | Daily Calories                 |
  |  •  Remaining: 1,200 kcal      |
  | [Add Entry (primary +)]        |
  |--------------------------------|
  | Recent                         |
  |  - Chicken salad   350 kcal    |
  |  - Banana          105 kcal    |
  ---------------------------------
  [Home][Search][ + ][Favorites][Me]

- Search
  ---------------------------------
  | < Back | Search bar           |
  | Suggestions: "rice", "chicken" |
  | -------------------------------|
  | [Thumb] Chicken breast         |
  |  Brand • 165 kcal / 100g       |
  | [Thumb] Brown rice             |
  ---------------------------------

- Food Detail (modal)
  ----------------------
  | Image                |
  | Name                 |
  | Brand • 165 kcal     |
  | Serving: [100g v]    |
  | Qty: [-] 1 [+]       |
  | [Add to diary]       |
  ----------------------

Design decisions (why)
- Mobile-first + bottom nav: quick thumb reach for common tasks.
- Card layout for results: scannable visual hierarchy for quick selection.
- Floating Add CTA: primary action on every screen to reduce friction adding entries.
- Defer barcode scanner: reduces MVP complexity and allows focus on core search UX.

Deliverables & assets
- This spec: output/design/diet_calorie_app_wireframes.md (this file)
- Next: Figma file + PNG exports (I will create and upload to repo/drive after quick art pass)

Notes for backend (for Marcus)
- UI expects these endpoints (examples):
  - GET /api/v1/foods?query=
  - GET /api/v1/foods/{id}
  - POST /api/v1/diary (payload: user_id, food_id, serving_size, quantity, timestamp)
  - GET /api/v1/users/{id}/favorites
  - POST /api/v1/users/{id}/favorites
- Keep response latency target <200ms for search.

Next steps
1. #ai-frontend (Kevin): Implement screens + responsive adjustments. Use tokens above.
2. #ai-backend (Marcus): Confirm endpoints and schema; API stubs to match component needs.
3. I'll create Figma + PNG exports within 24 hours and attach here.

Decision request for Alex
- Recommendation: Please start OpenAPI stub + SQL migrations now (aligns with design). Barcode scanner remains v1.1.


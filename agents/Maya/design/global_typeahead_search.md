# Global Typeahead Search — Spec

Author: Maya (Design)
Date: 2026-03-06

Purpose
- Reduce context-switching and speed up discovery for power users, PMs, and support by surfacing instant results across Users & Projects from the global header.

Acceptance criteria
- Keyboard + screen-reader accessible (ARIA roles, live regions).
- Debounce 300ms on input.
- Shows results and total_count, paginates or provides “See more”.
- Handles empty, loading, and error states gracefully.
- Perceived latency <200ms after backend responds.

Key decisions
- Input behavior: debounce 300ms, cancel previous requests on new keystroke.
- Results UI: unified list with type badges (User / Project), up to 10 results initially, with “See more” to open full search page (or infinite scroll up to 50 in dropdown).
- Keyboard: Up/Down to navigate items, Enter to open, Esc to close, Tab to focus next control.
- Accessibility: use role="combobox" + aria-expanded, listbox for results, active descendant; announce total_count via aria-live polite.
- Mobile: show compact search icon in header; tapping opens full-screen modal with same behavior.
- Microcopy: clear empty/error copy (see section below).

RICE scoring (assumptions)
- Reach: 40% of daily active users will use search at least once/day → Reach = 40k users/month.
- Impact: 7 (improves task speed for power users & support).
- Confidence: 75% (estimates based on product research & analytics).
- Effort: 5 person-weeks (frontend + backend + QA + design tweaks).
- RICE = (40,000 * 7 * 0.75) / 5 ≈ 42,000 (relative prioritization score).

Kano category
- One-dimensional (performance & quality of search directly increases satisfaction). For power users this becomes a must-have over time.

User flows
1) Desktop quick-search
  - User presses / or clicks search input.
  - Type starts, debounce 300ms fires query.
  - Dropdown shows up to 10 combined results with type badges, highlighted matches, and total_count.
  - Arrow keys move selection; Enter opens result; Shift-Enter opens in new tab.
  - If more than shown, last row is “See more results (N)” which opens full search page.

2) Mobile
  - Tap search icon → full-screen modal with input focused.
  - Same interactions; results stacked, larger touch targets.

Component specs
- Header search input
  - Placeholder: "Search people & projects (press /)"
  - Icon: magnifier, accessible label "Global search".
  - Clear button appears when text present.
- Dropdown card
  - Max height: 420px; overflow: auto (virtualize if >30 results).
  - Result row: avatar/icon, primary text (name/title), secondary meta (project owners, last updated), type badge (chip), subtle chevron for navigation.
  - Highlighting: wrap matched substring with <mark> or visually equivalent span; ensure screen reader reads full text.
- Keyboard nav
  - role="combobox" on input with aria-controls pointing to listbox id.
  - listbox children role="option" and aria-selected toggled.
  - aria-activedescendant to link active option.
  - aria-live region (polite) to announce "X results for 'QUERY'".

API (backend ask — summary)
- Endpoint: GET /api/v1/search?q=&type=(users|projects|all)&page=&per_page=
- Response: include results[], total_count, page, per_page, facets (optional), took_ms (for telemetry).
- Result shape: { id, type: 'user'|'project', title, subtitle, avatar_url, url, match_positions? }
- Pagination: offset or page-based; client default per_page=10.

Microcopy (default states)
- Loading: show skeleton rows; aria-busy on listbox.
- Empty: "No results for '{query}'. Try different keywords or check spelling."
- Error (offline/server): "Search unavailable. Check connection or try again later." Button: "Open full search" (fallback to full search page).
- See more row: "See more results ({total_count})"

Performance & UX polish
- Show local caching for repeated queries (LRU cache for recent 20 queries).
- Show interim optimistic UI for fast perceived response (progress bar/fade-in). Ensure perceived latency <200ms after backend sends response.
- If backend takes >500ms, show skeleton + subtle spinner.

Edge cases
- Rate limiting: show friendly message and fallback to full search.
- Partial results: show what we have + note "Showing top results".

Design deliverables
- Wireframes below (ASCII)

Desktop header dropdown (compact)

[ Header: Logo | Nav | search[🔍 Search people & projects] | avatar ]
                _______________________________
               | search query                 |
               |-------------------------------
               | • Alice Johnson (Product)     |
               | • Project Apollo (Repo)       |
               | • Ben K. (Support)            |
               |-------------------------------
               | See more results (54)         |
               -------------------------------

Mobile full-screen

[Full-screen modal]
[ < Back ]  [ Search input__________________ ]
[Results]
• Alice Johnson — Product Manager
• Project Apollo — 12 members
...

Implementation notes for frontend
- Debounce: 300ms. Cancel previous XHR/fetch on new query.
- Default per_page=10. Show up to 10, then See more.
- Keyboard and ARIA as specified.
- Use virtualization for long lists; but limit dropdown to 50 items.

Next steps
- Backend: define API contract and example responses + rate-limit behavior + per-type relevance scoring. (Assigned to Marcus).
- Frontend: implement dropdown + accessibility + mobile modal. (Assigned to Kevin).
- Design: validate microcopy and visual spacing in components.

Files
- This spec: output/specs/global_typeahead_search.md

Notes
- Decision rationale: unified results reduce modal switching and support quick discovery. Card-style rows keep scanning fast; chips for type reduce ambiguity.
- Open question: relevance weighting between Users vs Projects — default to recency + relevance score returned by backend; discuss with Marcus.


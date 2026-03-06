# Global Typeahead Search — Frontend contract & decisions

Summary
- Purpose: Define the exact fields and UI-related expectations the frontend needs from GET /api/v1/search for the global typeahead.
- File owner: Kevin (Frontend)

Decisions (final)
1) Highlight format: server SHOULD return snippet_html (string) containing matched terms wrapped in <em> tags (e.g. "... quick <em>brown</em> fox ..."). Additionally, server MAY include snippet_ranges: [{start: number, end: number}] for clients that prefer programmatic highlighting or accessibility use-cases. Frontend will sanitize and render snippet_html (only allow <em>).

2) Pagination format: server SHOULD return total_count (integer), page (integer, 1-based), per_page (integer). For cursors, include optional next_cursor if using cursor-based paging. Frontend will request per_page up to 10 for typeahead.

3) Result limit: frontend will display up to 10 results in the dropdown. If total_count > shown results, show a "See more" button that navigates to the full search results page (no infinite scroll in the typeahead).

4) Keyboard & ARIA: server should provide stable 'id' per item. Frontend requires id, title, snippet_html, url to implement keyboard focus and ARIA attributes correctly.

5) Debounce: frontend will debounce input 300ms (per spec).

Required response shape (example)
{
  "query": "brown",
  "page": 1,
  "per_page": 10,
  "total_count": 42,
  "items": [
    {
      "id": "doc_123",
      "title": "The Quick Brown Fox",
      "snippet_html": "The quick <em>brown</em> fox jumped...",
      "snippet_ranges": [{"start":10,"end":15}],
      "url": "/docs/doc_123",
      "type": "document",
      "icon_url": "https://.../doc-icon.svg",
      "score": 12.3,
      "metadata": {"created_at":"2025-11-01T12:00:00Z"}
    }
  ],
  "facets": {"type":{"document":30,"user":12}}
}

Security notes for Marcus
- If returning snippet_html, ensure only <em> tags are injected. Prefer server-side sanitization or returning escaped HTML with <em> inserted by server.
- Frontend will also sanitize with DOMPurify before injecting as innerHTML.

Frontend TODOs once API is ready
- Implement SearchTypeahead component (debounce 300ms, keyboard nav, ARIA, show up to 10 results, See more button)
- Tests: keyboard navigation, empty state, network error, long snippets

File path: output/specs/global_typeahead_search_frontend_fields.md

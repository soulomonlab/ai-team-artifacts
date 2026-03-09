# Header Search Component Specs

Components to implement (output/design/header_search_components.md)

1) SearchInput
- Props: placeholder, value, onChange, onClear, loading
- Height: 36px
- Padding: 8px 12px
- Left icon: search (24x24), Right icon: clear (16x16) visible when value
- States: idle, focus (outline #0366D6 2px), typing, loading (spinner substitute)
- Accessibility: role="combobox", aria-expanded, aria-controls, aria-activedescendant

2) ResultsDropdown
- Props: groups: [{label, items, viewAllUrl}], open
- Max width: 640px, min width: 320px
- Positioning: attached to input bottom with 8px gap, absolute, portal
- Z-index: 1000
- Each group: header (12px uppercase), items list
- Each group shows up to 5 items + optional "View all" link aligned to right

3) ResultItem
- Common props: id, type(user|content|doc), title, subtitle, meta, thumbnailUrl, onSelect
- Variants:
  - user: avatar 32px circle, title (14px semibold), subtitle (12px)
  - content: thumbnail 48px square, title, snippet (2 lines, ellipsis)
  - doc: doc icon 24px, title, path (secondary)
- Focus state: background #F3F4F6, aria-selected="true"
- Highlighting: render match tokens inside <mark> with class .search-highlight

4) EmptyState
- Message: "No results for 'xxx'"
- Suggest: "Try different keywords or check spelling"

5) LoadingSkeleton
- Placeholder rows with shimmer for each group (3 rows per group while loading)

Developer notes:
- Keep components stateless where possible; presentational only
- Provide utility to render highlighted text from match tokens (return React nodes)
- Ensure result container is keyboard navigable; manage focus with aria-activedescendant model


# Austria Guide App — Component Spec & Design Tokens (MVP)

목표
- Figma 구현 전 개발-디자인 정렬을 위해 주요 UI 컴포넌트와 디자인 토큰을 정의합니다.

디자인 토큰 (초안)
- 색상
  - primary: #0B64D6 (brand blue)
  - accent: #FF7A59 (cta)
  - bg: #FFFFFF
  - surface: #F6F8FA
  - text: #0F1724 (primary text)
  - muted: #6B7280
  - success: #10B981
  - warning: #F59E0B
  - error: #EF4444

- 타이포그래피
  - font-family: Inter (system fallback)
  - h1: 28px / 32px line-height / 700
  - h2: 22px / 28px / 600
  - body: 16px / 24px / 400
  - caption: 12px / 16px / 400

- 스페이싱 (base = 8px)
  - spacing-1: 4px
  - spacing-2: 8px
  - spacing-3: 16px
  - spacing-4: 24px
  - spacing-5: 32px

- 엘리베이션
  - card: 0 1px 2px rgba(16,24,40,0.04)
  - modal: 0 8px 24px rgba(16,24,40,0.12)

컴포넌트 목록 (구현 우선순위: High -> Medium -> Low)
1. Navigation Bar (Bottom) — High
   - Items: Home, Map, Itinerary, Profile
   - Icon size: 24px, Label: 10px
   - Active tint: primary, inactive: muted

2. Search Bar (Global) — High
   - Height: 44px, Corner radius: 8px
   - Left icon: search 20x20, placeholder color: muted
   - On focus: full screen Search results

3. City Card (Horizontal scroll) — High
   - Image ratio 3:2, Overlay gradient, Title bottom-left
   - Padding: spacing-3

4. POI List Item Card — High
   - Thumbnail 72x72, Title, subtitle, tags, actions (save, share)
   - Tap area: full card

5. Bottom Sheet (POI Detail) — High
   - States: peek (120px), half (60%), full (100%)
   - Drag handle 36x4 center
   - Background: bg, shadow: modal

6. Map Mini (Card) — Medium
   - Static preview with 'open map' CTA

7. Itinerary Timeline Item — High
   - Time chip on left, content card right, actions: edit, delete, drag handle

8. Modal / Share Sheet — Medium
   - Standard system modal with share options

9. Empty States / Error States — Medium
   - Illustration + short message + CTA

Interaction details & edge cases
- Save (favorite) action should show immediate optimistic UI change; if backend fails, show undo snackbar
- Offline map: show small 'Offline' badge and fallback CTA to download MBTiles; disable directions requiring network
- GDPR opt-in: On first app open, show concise modal with 'Accept' and 'Manage Preferences' — Accept enables analytics and personalization

Accessibility notes
- All interactive elements keyboard/touch accessible
- Contrast as above; focus states visible

Developer handoffs
- Provide token JSON (variables) in next iteration for direct import to Figma / styled-components
- Export assets: icons as SVG (24px/48px) — list provided in Figma file

파일: output/design/austria_design_components.md

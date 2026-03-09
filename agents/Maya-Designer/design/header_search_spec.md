# Header Search UX Spec

요약
- 목적: 헤더 검색 입력 및 결과 드롭다운 디자인 (데스크탑 + 모바일)
- 산출물: 사용자 흐름, 컴포넌트 명세, 와이어프레임(ASCII), 액세서빌리티/키보드 내비게이션, 반응형 동작, 에셋 내보내기 지침
- 파일: output/design/header_search_spec.md

1) 핵심 요구 (The real ask)
- 헤더에 들어가는 검색 입력창 디자인
- 결과를 그룹별(Users, Content, Docs)로 보여주기
- 검색어와 매칭되는 부분을 하이라이트
- 키보드 탐색(위/아래/Enter/Esc) 지원
- 모바일에서의 반응형/모달 처리
- Figma 원형 파일 + 에셋 내보내기 지침 제공

2) MECE로 나눈 하위 질문
A. 검색 입력 UX (placeholder, focus, clear, loading)
B. 결과 리스트 레이아웃 및 그룹화 (Users / Content / Docs)
C. 하이라이트 규칙 (매칭 텍스트 시각화)
D. 키보드 및 접근성(ARIA, focus 관리)
E. 모바일 대응 (헤더 컴팩트 vs 전면 모달)
F. 에셋/컴포넌트 규칙 (아이콘, 아바타, 썸네일)

3) 디자인 결정 요약 (짧게)
- 데스크탑: 드롭다운(포털) 형태로 바디 위에 떠서 결과 그룹을 노출. 이유: 빠른 피드백, 기존 헤더 흐름 유지.
- 모바일: 전체 화면 검색 모달(Top bar + 백 버튼). 이유: 작은 화면에서 입력과 결과 탐색을 방해하지 않음.
- 그룹별 우선순위: Users > Content > Docs (사용자 의도에 따라 인물 검색 우선)
- 하이라이트: 케이스 인센서티브 매칭(대소문자 무시), 매칭된 토큰에 <mark> 스타일 (노란색 대비) 적용.
- 키보드: 즉시 반응형 포커스 이동, Up/Down 순환(루프), Enter = 오픈, Esc = 닫기.

4) 사용자 흐름 (간단)
- 유저가 헤더 검색 입력에 타이핑
  - 0~2문자: 추천 검색어나 최근 검색 표시
  - >=3문자: 서버/로컬 검색 실행(debounce 250ms)
  - 결과 로딩: 스켈레톤/로딩 스피너 표시
  - 결과 수신: 그룹으로 렌더 → 각 항목 하이라이트 → 키보드/마우스로 선택 가능
  - 항목 선택: 엔터/클릭 → 상세 페이지로 이동
  - Esc 또는 배경 클릭: 드롭다운 닫힘

5) 컴포넌트 사양
- SearchInput (헤더)
  - 높이: 36px (컴팩트) / 아이콘(검색) 왼쪽, clear(X) 오른쪽
  - placeholder: "Search people, content, docs..."
  - 상태: idle / focus / typing / loading / error
  - accessibility: input role="combobox", aria-expanded, aria-controls -> results id

- ResultsDropdown (포털)
  - 최대 너비: 640px, 최소: 320px, 위치: input 하단 정렬, z-index 높은 포털
  - 그룹 헤더 스타일: label (uppercase, 12px, medium), 오른쪽에 "View all"
  - 항목 높이: 56px (avatars), 48px (compact)
  - 항목 구성: leading(avatar/thumbnail) | body(title + secondary) | trailing(meta or chevron)
  - 섹션 구분: subtle divider(1px, neutral-200)

- Result Item (variant: user, content, doc)
  - user: avatar 32px, title (name, 14px, semibold), subtitle (handle, 12px)
  - content: thumbnail 48x48, title, snippet (highlighted matching tokens, 2 lines ellipsis)
  - doc: document icon, title, path/breadcrumb

- Empty / No results
  - 안내 텍스트 + action(try different keywords). Suggest search tips.

6) 하이라이트 규칙
- 매칭 범위: 토큰 단위로 매칭. 예: "ann" -> "Annabelle", "Joann"에서 해당 부분에 하이라이트
- 스타일: background-color: #FFF4B1 (contrast checked), border-radius: 2px, padding-inline: 2px
- 여러 토큰 매칭 시 각 토큰 모두 하이라이트
- 스니펫(콘텐츠) 내 하이라이트는 가급적 문장 앞/중간을 유지하고, 2줄까지만

7) 키보드 내비게이션 & 접근성
- Behavior:
  - ArrowDown: 포커스 다음 항목으로 이동 (if none -> first)
  - ArrowUp: 이전 항목 (if none -> last)
  - Enter: 현재 포커스 항목 선택 (navigate)
  - Esc: 드롭다운 닫기, input에 focus 유지
  - Tab: 기본 탭 순서 유지 — Tab 시 결과 항목이 아닌 다른 포커스 가능한 요소로 이동 (단, Shift+Tab으로 input으로 복귀 가능)
  - Home / End 지원 권장
- ARIA:
  - input: role="combobox", aria-expanded="true|false", aria-haspopup="listbox", aria-controls="search-results"
  - results container: role="listbox", id="search-results"
  - item: role="option", aria-selected="true|false" when focused
  - use aria-activedescendant on input to point to currently focused item's id (preference for single-focus model)
- Focus management: 화면 리더 사용 시 input과 결과 간 포커스 일관되게 유지

8) 모바일 반응형
- Small screens (<600px)
  - 상단 전체 모달로 전환: 검색 입력이 화면 상단에 고정, 뒤로가기(arrow) 버튼 좌측, clear 우측
  - 결과: 그룹은 세로 스택, 각 아이템 터치 사이즈 최소 48px
  - 스와이프 다운 또는 백버튼으로 닫기
  - 키보드 열릴 때 리스트가 자동으로 리사이즈, 입력창은 상단 고정

- Tablet / Medium
  - 드롭다운 형태 허용하되 full-width 또는 input width 기반으로 확장

9) 시각적 토큰 (권장값)
- 색상
  - background: #FFFFFF
  - surface (dropdown): #FFFFFF
  - divider: #E6E6E6
  - text-primary: #111827
  - text-secondary: #6B7280
  - highlight-bg: #FFF4B1 (WCAG 대비 체크 권장)
  - focus-outline: #0366D6  (2px)
- 타이포그래피
  - body: Inter 14/20
  - small: Inter 12/16

10) 와이어프레임 (ASCII)
- Desktop (header inline)

  [Header ... | 🔍 [Search people, content, docs...] | Avatar]
                 -------------------------
                 | Users                > |
                 | • Alex Johnson       |
                 | • Maria Gómez        |
                 |-----------------------
                 | Content              > |
                 | • How to onboard...  |
                 | • Release notes 2.3  |
                 |-----------------------
                 | Docs                 > |
                 | • API /search        |

- Mobile (fullscreen modal)

  [< Back] [🔍 Search people, content, docs...] [ X ]
  -------------------------------
  Users
  • Alex Johnson
  • Maria Gómez
  Content
  • How to onboard new hires
  Docs
  • API /search

11) 에지케이스 & 퍼포먼스
- 네트워크 지연: 250ms 내로 결과 없으면 스켈레톤 -> timeout 메시지
- 대량 결과: 각 그룹에 최대 5개 항목 렌더, "View all" 링크로 전체 검색 페이지로 이동
- 보안: 검색 결과에 민감 정보 노출 금지 (backend 가 책임)

12) Figma & 에셋 내보내기 지침
- 파일 구조
  - 페이지: 1) Components 2) Desktop – Header 3) Mobile – Modal 4) Tokens
  - 컴포넌트: SearchInput (variants: idle/focus/loading/with-results), ResultItem (variants: user/content/doc), ResultsSection
- 컴포넌트 규칙
  - 컴포넌트를 Auto Layout으로 제작 (padding tokens 사용)
  - Variant로 state 관리
- 에셋 내보내기
  - 아이콘: search.svg, clear.svg, chevron-right.svg (24px), doc-icon.svg, user-avatar-default.png (32x32)
  - 썸네일: content-thumb@2x.png — export 48x48 and 96x96
  - 방법: 각 아이콘을 SVG로 export, JPG/PNG는 2x 해상도로 export
- Figma 링크: 디자인 파일을 생성하고 공유 링크를 여세요. (팀 가이드: ‘Can view’ 이상 권한으로 공유)

13) Acceptance Criteria (QA)
- 입력 후 250ms debounce 내에 서버 요청 발생
- 키보드로 모든 결과 항목에 도달 가능 (Up/Down/Enter/Esc 동작 검증)
- 그룹별로 결과가 표시되고, 각 그룹에 최대 5개 항목이 보임
- 하이라이트 스타일이 지정한 토큰 색상으로 적용
- 모바일에서 검색은 전체 화면 모달로 동작

14) 구현 메모 / 디자이너 코멘트
- 하이라이트 색상 대비가 충분치 않으면 더 짙은 옐로우(#FFE08A) 권장
- 텍스트 래핑: title은 1줄, snippet은 2줄로 자르기
- AVATAR: 라운드 50%

---
디자인 파일 생성 후 Figma 링크를 여기 업데이트해주세요. 구현 시 컴포넌트와 토큰을 재활용하도록 권장합니다.

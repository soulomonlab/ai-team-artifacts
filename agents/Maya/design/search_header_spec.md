결론 (Summary)
- 헤더 검색 UX 및 결과 드롭다운 디자인 완성: 입력 필드, 결과 그룹화(Users, Content, Docs), 매치된 텍스트 하이라이트, 키보드 내비게이션, 모바일 반응형 규칙 포함.
- 산출물: output/design/search_header_spec.md (이 파일), Figma 파일 템플릿 링크(플레이스홀더) 및 내보낼 에셋 목록 포함.

프로젝트 목표
- 직관적이고 빠른 검색 경험 제공
- 결과 스캔성이 높아 사용자가 원하는 항목으로 빠르게 이동
- 데스크탑과 모바일에서 일관된 경험 유지

대상 사용자
- 로그인한 내부 사용자(팀원)
- 문서/콘텐츠를 자주 찾는 파워유저
- 가벼운 검색으로 사용자 프로필을 찾는 경우

요구사항 요약
- 입력: 즉시 검색 시작(타이핑 시 API 호출, debounce 200ms)
- 결과 그룹화: Users, Content, Docs (각 그룹 최대 5개 항목 표시, 더보기 링크)
- 매치 하이라이트: 단어 단위 강조(볼드 + 주황색 하이라이트 배경 옵션)
- 키보드 내비게이션: Tab, Up/Down, Enter(선택), Esc(닫기), Home/End(그룹 내 이동)
- 모바일: 전체 화면 오버레이 검색 모드 + 그룹 토글
- 접근성: aria roles, focus management, screen reader announcement

사용자 플로우
1) 사용자가 헤더 검색 입력을 클릭하거나 '/' 단축키로 포커스.
2) 입력 시 debounce(200ms) 후 검색 API 호출(키워드, limit per group).
3) 응답을 받아 그룹별로 결과 랜더링. 매치된 텍스트 하이라이트.
4) 사용자는 마우스 클릭 또는 키보드로 항목 선택. Enter: 선택 동작(페이지 이동 or 모달).
5) Esc 또는 외부 클릭 시 드롭다운 닫힘. 모바일에서는 상단 X 버튼으로 닫음.

와이어프레임 (ASCII)
- 데스크탑 (헤더에 내장된 드롭다운)

[Header] ------------------------------ [Search input ▾ ]
                      | Dropdown (max-width: 720px)
                      | ----------------------------------------------
                      | Users                    | Content               
                      | - @jin (Product)         | - How to design...    
                      | - @lee (Engineering)     | - Release notes...    
                      | ---------- See all Users ----------
                      | Docs                     |                      
                      | - API Guide              |                      
                      | ----------------------------------------------

- 모바일 (전체화면 오버레이)

[Top bar: < Back | Search input (full width) | X ]

[Results]
- Users
  • @jin — Product
  • @lee — Engineering
  • See all Users →
- Content
  • How to design header search...
  • Release notes v2...
- Docs
  • API Guide

컴포넌트 스펙
1) Search Input (HeaderSearchInput)
- 높이: 40px (데스크탑), 48px (모바일)
- padding: 0 12px
- border-radius: 8px
- placeholder: "Search people, content, docs..."
- 아이콘: left = magnifier (16px), right = clear (16px, visible when text exists)
- 상태: idle, focused(블루 테두리), loading(스피너 우측)
- HTML: <input role="search" aria-label="Header search" />

2) Dropdown (SearchResultsDropdown)
- 최대 너비 720px, min-width 320px, border-radius 12px
- 그림자: 0 8px 24px rgba(16,24,40,0.08)
- 그룹 간 구분선: 1px #E6E8F0
- 항목 높이: 56px (avatar + title + subtitle)
- 애니메이션: fade + translateY(6px), duration 160ms

3) Group (ResultGroup)
- 헤더: 그룹명(예: Users) + optional count + 'See all' action (link)
- 각 그룹은 최대 5개 항목 노출, 더 많을 경우 'See all' 노출

4) Item (ResultItem)
- 레이아웃: avatar(32px) | title(14/semibold) + subtitle(12/regular)
- 매치 하이라이트: <mark> 요소 스타일 — background: #FFF2D9 (soft orange), font-weight: 600
- 키보드 포커스: 배경 #F0F7FF, outline none, box-shadow inset 0 0 0 2px #D0E8FF
- 클릭 영역: full width
- 데이터: id, type, title, subtitle, url, highlight_ranges

매치 하이라이트 규칙
- 가장 긴 연속 매치 우선 하이라이트
- 여러 매치 있을 때는 각 매치별로 하이라이트
- 하이라이트는 HTML safe (escape) 적용 후 span/mark으로 감싼다

키보드 내비게이션
- 포커스 진입: input focus → 첫 번째 결과에 highlight focus하지 않음(유저가 Tab으로 이동 시 focus 이동)
- ArrowDown: 포커스를 다음 결과 아이템으로 이동
- ArrowUp: 이전 아이템으로 이동
- Enter: 현재 포커스 아이템 선택(기본 click 동작)
- Tab: 기본 탭 체인 유지하지만 드롭다운이 열려있는 동안 Tab은 다음 interactive element로 이동 (e.g., See all link, clear button). Shift+Tab으로 반대 이동.
- Esc: 드롭다운 닫기 & input blur
- Home/End: 그룹 내 시작/끝으로 이동
- 키보드 포커스 상태는 aria-activedescendant와 role="listbox" + role="option"을 사용해서 관리 권장

접근성 (A11y)
- Dropdown: role="listbox" aria-label="Search results"
- Item: role="option" aria-selected="true|false" aria-label="{type}: {title}"
- Live region: 검색 결과 업데이트 시 screen reader에게 "검색 결과: Users 3개, Content 2개" 같은 짧은 문구로 aria-live="polite" 영역에 노출
- Contrast: 텍스트 대비 WCAG AA 준수(본문 최소 4.5:1)
- Focus trap는 사용하지 말 것(사용자가 자유롭게 탭 이동 가능하도록)

모바일 반응형 규칙
- 트리거: 헤더의 검색 아이콘 탭 → 전체 화면 오버레이(검색 전용)
- 오버레이: 상단 고정 검색바, 결과는 아래 스크롤 영역. 그룹을 아코디언처럼 접을 수 있음.
- 내비게이션: 터치 대상 최소 44x44dp
- 애니메이션: 모달 슬라이드 업 180ms

시각 디자인 핵심값
- 색상: Primary text #0F1724, Secondary #6B7280, Highlight background #FFF2D9, Focus bg #F0F7FF
- 타이포그래피: Inter / 14px(제목), 12px(부제)
- 아이콘: 단색(현재 컬러) + 16px

에지케이스
- No results: 그룹별로 "No results" 메시지 또는 전체 결과 없음 카드(추천 키워드 3개)
- Slow network: skeleton UI(3 rows)과 spinner 표시
- Empty query: 최근 검색 또는 추천 검색(최근 5개)

내보낼 에셋 (개발용)
- icons/search-16.svg
- icons/clear-16.svg
- avatars/default-32.png
- ui/highlight-bg-1.png (optional tiny texture)
- animations/dropdown-open.json (Lottie) — optional
(프론트엔드에서 SVG 스프라이트 또는 아이콘 컴포넌트로 합칠 것 권장)

Figma
- Figma 템플릿 파일(플레이스홀더): https://www.figma.com/file/PROJECT_SEARCH_HEADER (생성 후 링크 업데이트 필요)
- 페이지: Desktop / Mobile / Tokens / Assets
- 권장: 컴포넌트화(Headless patterns): HeaderSearchInput, SearchDropdown, ResultGroup, ResultItem

구현 가이드 (개발팀에 주는 핵심 포인트)
- 서버: 그룹별 limit 적용(예: users:5, content:5, docs:5) + total counts
- 클라이언트: highlight_ranges를 받아서 텍스트에 안전하게 적용
- CSS: prefers-reduced-motion 사용 고려
- 테스트: keyboard navigation 시 연속성, screen reader announcement

수락 기준 (Acceptance criteria)
- 데스크탑: 타이핑 후 결과가 200ms 내에 debounce로 호출되어 그룹별 결과가 표시된다
- 키보드: Arrow keys, Enter, Esc 모두 동작한다
- 모바일: 전체화면 오버레이로 전환되며 터치 타깃이 기준을 만족한다
- 접근성: aria 속성과 live region으로 스크린 리더가 결과 변화를 인지한다

결정 기록(Decision log)
- Debounce 200ms 선택 이유: 즉각성 vs API 과다 호출 균형(측정된 트래픽 기준)
- 그룹 상한 5개: 스캔성 확보 및 레이아웃 안정성 확보
- 하이라이트 색상: 시각적 우선순위를 주되 대비 규칙 준수

다음 단계
- 이 문서 기반으로 Figma 파일 생성 및 컴포넌트화 -> 프론트엔드로 전달
- 프론트엔드는 React로 컴포넌트 구현 및 accessibility 테스트 수행

파일 위치
- output/design/search_header_spec.md (현재 파일)

문의/디자인 검토 요청
- 세부 UI 토큰 또는 색상 조정이 필요하면 바로 피드백 주세요. 특정 브랜딩 색상 반영 가능합니다.

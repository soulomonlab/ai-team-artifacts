# Frontend Typeahead UI Spec

요약
- 핵심 결정: 하이라이트 포맷은 HTML <em> 태그 사용. 범위(ranges) 포맷은 폴백으로 지원.
- 탐색 UX: 'See more' 페이징(명시적 더보기) 선택 — 예측 가능성, 접근성, API 호출 제어 때문에 우선.
- 기대 API 필드(프론트엔드 필요): id, title, highlight_html, snippet, type, url, score, total_count, page, per_page.
- 동작 제약: 디바운스 300ms, 최소 2자 입력에서 검색 시작, 결과 최대 10개 표시.

배경 및 목적
- Marcus가 작성한 백엔드 스펙(output/specs/global_typeahead_search.md)을 검토한 결과, 프론트엔드는 하이라이트 렌더링 방식과 페이징 UX 결정을 명확히 해야 백엔드가 API 응답을 확정할 수 있음.

결정(Resolution) — 결론 우선
1) 하이라이트 포맷: HTML <em> 태그 사용
   - 이유: 서버에서 이미 하이라이트 태그를 주입하면 프론트엔드는 렌더링만 하면 되어 구현이 간단하고 일관성 있음.
   - 보안 대비: 서버에서 전달한 highlight_html을 클라이언트에서 innerHTML로 렌더링하려면 반드시 DOMPurify 같은 라이브러리로 sanitize 후 삽입.
   - 대안(폴백): 서버가 ranges(문자 인덱스)를 제공하는 경우 프론트엔드에서 텍스트를 다시 조합해 <em>로 감싸는 유틸을 제공.

2) 'See more' vs Infinite Scroll: 'See more'(명시적 더보기) 선택
   - 이유: 즉시 불러오는 infinite scroll은 예측 불가한 API 호출(비용+레이트 제한)과 접근성 이슈가 있어 우선순위 낮음.
   - 구현: Typeahead 결과 하단에 "See more" 버튼/링크 노출(총 개수 표시: "See more — 234 results") → 클릭 시 전체 검색 결과 페이지(/search?q=...] 또는 /search?query=&page=1)로 이동하거나, 프론트에서 page=2 호출하여 결과를 확장.

API 응답에서 프론트엔드가 필요로 하는 필드(권장)
- id: string — 항목 고유 식별자
- title: string — 주요 텍스트(렌더링 대상)
- subtitle?: string — 보조 텍스트(옵션)
- highlight_html?: string — 서버가 제공하는 하이라이트 HTML(예: "This is a <em>match</em>.")
- snippet?: string — 일반 텍스트 요약(하이라이트가 없을 때 사용)
- type?: string — 결과 타입(예: "article", "user") — 아이콘/메타표시용
- url?: string — 엔트리로 이동할 링크
- score?: number — 정렬/재현성용(선택)
- total_count: number — 전체 결과 수(See more 렌더링 판단)
- page: number — 현재 페이지
- per_page: number — 페이지당 항목 수

하이라이트 처리 권장 방식
- API 제공: highlight_html 필드로 <em> 태그 포함 HTML 제공.
- 프론트엔드 렌더링:
  1. 서버에서 받은 highlight_html에 대해 DOMPurify.sanitize(highlight_html, {ALLOWED_TAGS: ['em']}) 를 호출.
  2. sanitized HTML을 안전하게 렌더링(dangerouslySetInnerHTML) — React 환경에서는 반드시 sanitize 후 삽입.
- 폴백(서버가 ranges만 제공할 경우): ranges 배열을 받아 텍스트를 분해하고 <em>로 감싸서 동일한 HTML 출력 생성.

UX / Accessibility (핵심)
- Input
  - aria-controls 연결: input[aria-controls="typeahead-list"]
  - role="combobox" 및 aria-expanded 상태 관리
- List
  - ul[role="listbox"] id="typeahead-list"
  - li[role="option"] 각각에 aria-selected 설정
  - 활성 항목은 포커스 스타일과 aria-activedescendant 사용 권장
- Keyboard
  - ArrowDown/ArrowUp: 항목 이동
  - Enter: 현재 선택 항목으로 이동(open URL)
  - Escape: 팝업 닫기 + 포커스 input로 복귀
  - Home/End(선택): 맨 위/맨 아래로 이동
- Screen reader: 각 항목에 텍스트 + ", X of Y" 식으로 순서 안내(선택적)

비헤이비어 및 엣지케이스
- 최소 입력 길이: 2자 미만이면 요청하지 않음
- 디바운스: 300ms(설정값으로 노출)
- 결과 수 제한: 최대 10개 표시
- 로딩 상태: 스피너 또는 skeleton
- 빈 결과: "No results for \"{query}\""
- 오류(429 레이트 제한): 사용자에게 짧은 메시지("Too many requests, try again in a moment")와 재시도 제안
- 네트워크 실패: 친절한 재시도 버튼

Acceptance criteria (프론트엔드 구현 기준)
- Typeahead 컴포넌트 구현(React + TSX)
  - 입력 디바운스 300ms, 최소 2자
  - 최대 10개 결과 렌더
  - highlight_html을 안전하게 렌더(또는 ranges 폴백)
  - 키보드 내비게이션 및 ARIA 지원
  - "See more" 노출(총 개수 기반)
- 테스트: 키보드 동작, highlight 렌더링, 로딩/빈/에러 상태

개발자 메모 / 백엔드 요청 사항(Marcus에게)
- highlight_html 필드에 <em> 태그로 하이라이트를 주입해 주세요(또는 ranges 둘 다 제공). API는 HTML 인젝션 리스크를 줄이기 위해 태그 이스케이프/화이트리스트 규칙을 문서화해야 합니다.
- total_count 필드를 포함해 주세요(See more 여부 판단용).
- 페이징 파라미터: page, per_page 또는 next_page 토큰 중 하나를 명시해 주세요. 프론트는 page/per_page가 가장 간단합니다.

파일/경로
- 이 문서는 프론트엔드 타입어헤드 UI 사양입니다. (output/specs/frontend_typeahead_ui.md)

다음 단계
1. Marcus: API에 highlight_html 및 total_count, page/per_page 포함 여부 확정해 주세요.
2. Kevin(프론트): 해당 응답 스키마를 받는 즉시 Typeahead 컴포넌트 구현 시작(테스트 포함).


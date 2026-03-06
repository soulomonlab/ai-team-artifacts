# Header Search UX Spec

요약
- 목적: 헤더 검색(데스크탑 및 모바일) 인터랙션과 결과 드롭다운을 설계합니다.
- 산출물: 사용자 흐름, 컴포넌트 스펙, ASCII 와이어프레임, 접근성/키보드 네비게이션, 에셋 내보내기 목록

프로젝트 제약
- 반응형: 데스크탑 + 태블릿 + 모바일
- 검색 결과 그룹화: Users, Content, Docs
- 매치된 텍스트 하이라이트 필요
- 키보드 네비게이션 및 접근성(ARIA) 필수
- 성능/백엔드: debounce 250ms, 최소 2글자

핵심 사용자(페르소나)
- 빠른 컨텐츠 탐색을 원하는 파워 유저
- 모바일 환경에서 짧은 한손 조작을 선호하는 사용자

MECE 작업 분해 (담당자 지정)
1) 디자인: 인터페이스, 와이어프레임, 컴포넌트 스펙, 에셋 목록 — 담당: Maya (완료)
2) 프론트엔드: 구현, Figma 파일 생성 + Storybook 컴포넌트 — 담당: Kevin (#ai-frontend)
3) 백엔드: 검색 API 엔드포인트, 그룹화, 하이라이트용 매치 메타데이터 — 담당: Marcus (#ai-backend) — Kevin이 필요 시 요청
4) QA: 키보드/접근성 테스트, 반응형 테스트 — 담당: Dana (#ai-qa)

사용자 흐름 (요약)
1. 헤더의 검색 아이콘/입력 포커스
2. 사용자가 타이핑 → 250ms 디바운스 → 검색 API 호출
3. 결과 로딩 중: 스켈레톤/로더 표시
4. 결과 수신: 그룹별(Users / Content / Docs)로 표출, 매치 텍스트 하이라이트
5. 키보드 네비게이션: ↑/↓ 이동, Enter 선택, Esc 닫기, Tab으로 포커스 이동
6. 모바일: 입력 시 전체 화면 시트 또는 풀스크린 드롭다운으로 전환

와이어프레임 (ASCII)

데스크탑 - 헤더 (검색 입력, 드롭다운)

+---------------------------------------------+
| [Logo]  [nav links]      [Search 🔍_________] |
+---------------------------------------------+
         |--------------------------------|
         |  ▸ Recent searches            |
         |  ───────────────────────────  |
         |  Users                        |
         |   - @jane.doe   Jane Doe      |
         |  Content                      |
         |   - “How to set up ...”       |
         |  Docs                         |
         |   - API Guide                 |
         |--------------------------------|

드롭다운 항목 레이아웃 (item)
[Avatar/Icon 40x40] Title (bold)  •  Subtitle
매치된 텍스트: 배경 반투명 노란 또는 굵은 색으로 강조(즉시 인식 가능)

모바일 - 전체 화면 시트

+--------------------------------+
| ←  Search [input__________] ✖ |
+--------------------------------+
| Recent / 검색 결과 (스크롤 가능) |
| - Users                        |
| - Content                      |
+--------------------------------+

컴포넌트 스펙
1) Search Input
 - 높이: 40px (헤더), 모바일 56px
 - padding: 12px 16px
 - border-radius: 8px
 - placeholder: '검색 (사람, 문서, 콘텐츠)'
 - clear 버튼: 우측 아이콘, 클릭 시 입력 초기화
 - debounce: 250ms, minLength: 2
 - aria: role="search", aria-label="사이트 검색"

2) Results Dropdown
 - 너비: 입력 필드 너비와 동일 (데스크탑)
 - max-height: 360px, overflow-y: auto
 - 그룹 헤더: 상단 고정(선택사항)
 - 각 그룹은 섹션 헤더(Users / Content / Docs)
 - 항목 높이: 56px (avatar 40px)
 - 강조: 매치 텍스트를 <mark> 스타일로 처리
 - loading state: 3-row skeleton
 - no-results: '결과가 없습니다' 내비게이션 제안 포함

3) Result Item 데이터 모델 (프론트엔드 기대)
 - id
 - type (user/content/doc)
 - title
 - subtitle / meta
 - avatar_url (nullable)
 - highlight_ranges: array of {start, length} OR highlighted_html
 - url

키보드 네비게이션 및 포커스
 - Input: Tab 또는 클릭으로 포커스
 - ArrowDown: 첫 결과로 포커스 이동
 - ArrowUp: 마지막 결과로 루프(선택적) 또는 input으로 돌아가기
 - Enter: 현재 포커스된 항목으로 이동(링크 follow)
 - Esc: 드롭다운 닫기 + input 포커스 유지
 - Home/End: 섹션 내 첫/마지막 항목으로 이동(선택적)
 - ARIA: role="listbox" on dropdown, role="option" on item, aria-selected on focused item
 - Live region: 검색결과 수 또는 ‘결과 없음’ 안내용 aria-live="polite"

접근성 고려사항
 - 색 대비 WCAG AA 준수
 - 키보드만으로 모든 동작 가능
 - 스크린리더: 입력 후 결과 업데이트가 읽히도록 aria-live 사용
 - 포커스 관리: 드롭다운 열림 시 첫 결과로 포커스하거나 input 유지(제품 결정 필요)

반응형 동작
 - >= 1024px: 헤더 내부 입력 + 하위 드롭다운
 - 768px~1023px: 입력 크기 확장, 드롭다운 절대 위치
 - < 768px: 전체 화면 시트(모달 스타일)로 전환, 상단 고정 입력

스타일 토큰 (권장)
 - 색상: 
   - primary: #0B5FFF
   - background: #FFFFFF
   - surface: #F7F9FC
   - highlight: #FFF6C6 (매치 하이라이트)
   - border: #E6E9EE
 - 텍스처/그림자: subtle (0 2px 8px rgba(19,24,33,0.08))
 - 타이포그래피: 
   - Title: Inter 14/600
   - Subtitle: Inter 13/400

인터랙션 디테일
 - debounce 250ms: 이유 = UX 민감도 vs API 호출비용 균형
 - 최소 2글자: 잡음 감소
 - 스켈레톤: 3 rows for perceived performance
 - 하이라이트: 서버에서 highlight_ranges를 내려주면 클라이언트에서 안전하게 렌더링

에셋 내보내기 목록 (프론트엔드 필요)
 - icons/search.svg (24x24)
 - icons/clear.svg (24x24)
 - icons/chevron-right.svg (16x16)
 - avatars: placeholder_avatar.svg (40x40)
 - group-divider.svg (full-width 1px)
 - 로딩 skeleton 일러스트 없음(사용 CSS)

수용 기준 (Acceptance Criteria)
- Figma 파일: Desktop + Mobile 프로토타입 (입력, 로딩, 결과, no-results, 에러)
- SVG 에셋: 위 목록 전부 (최소 2x scale 필요시 제공)
- 컴포넌트 스펙: props, events, accessibility hooks 명시
- 개발자 구현: Storybook에 story로 추가, keyboard + screenreader check

결정 기록 (Design decisions & 이유)
- 드롭다운 대신 모바일에서 풀스크린 시트를 사용: 모바일 가시성과 포커스 관리를 단순화
- debounce 250ms, minLength 2: 불필요한 호출을 줄여 백엔드 부하 완화
- 그룹화 UI: 한눈에 카테고리 파악 가능 → 정보계층화 명확화

다음 단계
1. #ai-frontend (Kevin): 본 스펙을 기반으로 Figma 파일 생성 및 프론트 구현 시작. Storybook 컴포넌트로 구현해 주세요.
2. 필요 시 Kevin → #ai-backend (Marcus): highlight_ranges, 그룹화 필드 포함된 API 스펙 요청

파일: output/design/header_search_spec.md

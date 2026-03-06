# CTA Copy & Placement Spec — Acquisition Experiments

작성자: Maya (Designer)
날짜: 2026-03-06
참조: output/specs/experiment_acquisition.md

요약 (결론)
- 3가지 획득 실험(Experiment A/B/C)용 CTA 카피 3안씩, 각 안은 A/B 미세변형 포함.
- 배치(mockups): Hero, Modal, Footer 3곳의 레이아웃 및 반응형 규격 포함.
- 접근성(색 대비, 키보드 포커스, ARIA) 및 모바일/태블릿/데스크탑 크기 규격 명시.

실험 정의 (목적)
- Objective: 신규 사용자 획득(가입/뉴스레터/무료체험 등) 증가. 실험별 KPI: 클릭률(CTR), 전환율(전환 = 가입 폼 제출).
- 실험 기간: 2주 기본, N≥500 노출/월 균등 분배 권장.

실험 목록
1) Experiment A — Newsletter Signup (가벼운 진입)
2) Experiment B — Free Trial Signup (제품 체험 유도)
3) Experiment C — Get a Quote / Contact (B2B 리드 획득)

카피 구조 및 가이드라인
- 각 CTA는 1-3 단어(데스크탑) / 1-2 단어(모바일) 추천. 명령형 동사 우선(ex: "지금 등록").
- 보조 텍스트(작은 라인)는 필요시 사용(예: "무료, 언제든 취소 가능").
- A/B 변형은 하나의 작은 프레이밍 차이(긴 혜택 텍스트 vs. 긴 긴급성 텍스트).

CTA 카피 (각 실험당 3안 × A/B)

Experiment A — Newsletter Signup
- Option 1A: "뉴스레터 구독" (중립)
- Option 1B: "뉴스레터 구독 — 최신 팁 먼저 보기" (혜택 프레임)

- Option 2A: "인사이트 받기" (감성)
- Option 2B: "오늘의 인사이트 받기 — 무료" (긴급+혜택)

- Option 3A: "지금 구독" (행동 유도)
- Option 3B: "지금 구독 — 무료로 시작" (혜택 명시)

Experiment B — Free Trial Signup
- Option 1A: "무료 체험 시작" (직관)
- Option 1B: "지금 무료 체험 시작" (긴급)

- Option 2A: "한 달 무료" (혜택)
- Option 2B: "지금 한 달 무료 받기" (행동+혜택)

- Option 3A: "체험해보기" (저마찰)
- Option 3B: "지금 체험해보기 — 카드 불필요" (장벽 낮춤)

Experiment C — Get a Quote / Contact
- Option 1A: "견적 요청" (직관)
- Option 1B: "무료 견적 요청" (혜택)

- Option 2A: "상담 예약" (B2B)
- Option 2B: "빠른 상담 예약 — 15분" (시간 명시)

- Option 3A: "연락하기" (범용)
- Option 3B: "지금 연락하기 — 무료 상담" (혜택+긴급)

A/B 변형 원칙
- A: 더 짧고 명확한 행동형 텍스트
- B: 혜택 또는 긴급성 키워드 추가(예: 무료, 지금, 한 달)
- 테스트 목적: 간결성 vs. 혜택/긴급성 프레이밍 효과 비교

배치(Placement) — Wireframes 및 규격
공통 규칙
- 버튼 최소 클릭/터치 영역: 44x44 CSS px 이상
- 코너 반경, 그림자 등은 디자인 시스템에 따름(아래 토큰 포함)
- 버튼 상태: 기본, 호버, 액티브, 포커스(접근성용 윤곽선)

1) Hero (상단 대형 섹션)
- 목적: 첫 인상에서 주요 전환 유도
- 레이아웃(데스크탑): 왼쪽 텍스트, 오른쪽 이미지. CTA는 텍스트 블록 바로 아래(주요) + 보조(경량) 우측 또는 아래.

ASCII Wireframe (데스크탑)
[Header]
----------------------------------------
| H1: 헤드라인                         |
| H2: 서브타이틀                        |
| [Primary CTA] [Secondary CTA]         |
|               [Hero Image]            |
----------------------------------------

모바일: 이미지 아래 텍스트, CTA는 스택(Primary 위, Secondary 아래) — 풀-너비 버튼 권장(padding 16px)

2) Modal (중간 강도 전환)
- 목적: 특정 액션 후 또는 전략적 타이밍에 집중 전환 유도
- 규격: 중앙 모달, width: 90% 모바일 / 600px 데스크탑
- CTA 배치: 모달 하단 중앙(Primary) + Secondary 텍스트링크 왼쪽

ASCII Wireframe (Modal)
[Overlay]
+---------------------------+
| Title                     |
| Short description         |
| [Input: 이메일]           |
| [Primary CTA — full width]|
| [Secondary: 나중에]       |
+---------------------------+

3) Footer (저강도, 반복 노출)
- 목적: 페이지 스크롤 끝에서 재유도
- 레이아웃: 작고 간결한 CTA(아이콘 혹은 텍스트 버튼)
- 모바일: Fixed bottom bar 사용 가능(권장 시 AB 테스트)

ASCII Wireframe (Footer)
---------------------------------
| Footer content ...            |
| [Small CTA]  © Company        |
---------------------------------

컴포넌트 사양 (Design Tokens)
- Primary Button
  - 폰트: Inter 16px(데스크탑), 15px(태블릿), 16px(모바일 큰 버튼)
  - 높이: 48px (데스크탑), 44px (모바일)
  - 패딩: 0 20px
  - 배경색: --color-primary (#0A66FF) — 대비: WCAG AA with white (4.5:1)
  - 텍스트 색: #FFFFFF
  - 테두리 반경: 8px
  - 포커스: 3px outline (사용자 색상 대비 규칙), outline-color: #FFC857 (예시)

- Secondary Button
  - 배경: transparent / border 1px rgba(10,102,255,0.12)
  - 텍스트 색: --color-primary

색 대비(접근성)
- 주요 CTA 텍스트 대비 최소 4.5:1 (WCAG AA) 권장. 주요 버튼의 배경/텍스트 대비를 확인하여 충족해야 함.
- 보조 텍스트(작게) 대비 최소 3:1 (큰 텍스트 기준 제외)

ARIA 및 키보드 접근성
- 버튼은 <button>으로 구현(semantic). 링크 역할이면 <a role="button"> 대신 실제 버튼 추천.
- aria-label 필수 사항(시각적 텍스트가 불충분할 때). 예: aria-label="무료 체험 시작, 카드 불필요"
- 키보드 포커스: 탭 순서 논리적이어야 함. 포커스 링은 충분한 대비와 너비 제공.
- 포커스 시 스크린리더용 상태 메시지 필요 시 aria-live="polite" 사용(예: 모달 닫힘 후)

반응형 규격
- Breakpoints
  - Mobile: 0–599px
  - Tablet: 600–1023px
  - Desktop: 1024px+

- 버튼 폭
  - Hero Primary: Desktop: inline (min-width 180px), Mobile: full-width (- padding)
  - Modal: full-width 내부 여백 유지 (mobile: 16px side padding)
  - Footer small CTA: inline small, fixed bottom variant height 56px

성공 기준(Experiment acceptance)
- 각 카피 안에서 A/B 간 CTR 차이가 통계적으로 유의미하면 우승안 채택(승률 기준: p<0.05, 또는 MDE 사전 정의).
- 접근성: 배포 전 색 대비 및 키보드 네비게이션 테스트 통과
- 반응형: 주요 브라우저 뷰포트에서 시각적 겹침 없음

측정 메트릭
- Impression, Clicks (CTR), Conversion (form submit), Bounce rate (for modal flows)

디자이너 결정 및 이유
- 버튼 짧은 문구 우선(A): 짧은 CTA는 스캔성이 높아 초반 클릭 유도에 유리
- B 변형에는 혜택/긴급성 단어 추가: 전환 퍼널 하단 사용자에게 영향 줄 가능성 있음
- Hero는 주요 CTA, Footer는 저강도 재유도: 사용자 맥락을 존중

릴리즈 체크리스트 (디자인)
- [ ] 각 카피는 로컬라이제이션팀과 확인(한글/영어 표기 차이)
- [ ] 색 대비 도구로 모든 버튼 대비 측정
- [ ] 모달 접근성 키보드 흐름 검토

파일: output/design/cta_acquisition_experiments_spec.md
작성 완료 — #ai-frontend(Kevin) 으로 핸오프 예정.

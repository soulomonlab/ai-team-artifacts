# Diet Calorie App v1 — Mobile-first Design Spec

작성자: Maya (Designer)
목표: 모바일 우선 UX 와 직관적인 식단 칼로리 추적 흐름을 위한 와이어프레임, 컴포넌트 스펙, 상호작용 및 접근성 노트 제공.

요구사항(요약)
- 주요 화면: 온보딩, 검색(Search), 음식 상세(Food Detail), 식사 기록(Meal Logging), 일일 요약(Daily Summary), 설정(Settings: 칼로리 목표)
- 출력물: 디자인 스펙 문서(이 파일), Figma 파일(생성 필요), 키 스크린 PNG (export_presets.md 참조)

사용자 페르소나
- 빠르게 입력하고 기록하려는 직장인(Primary)
- 음식 검색 및 자세한 영양 정보를 확인하려는 건강 관심자(Secondary)

핵심 UX 목표
- 빠른 식사 기록(검색 → 선택 → 수량 → 저장) — 3단계 이내
- 명확한 시각적 계층(칼로리 목표 대비 진행률 강조)
- 접근성(고대비, 충분한 탭 영역, 레이블)

정보 구조(상위 수준)
1. 온보딩: 계정 생성(옵션) → 칼로리 목표 설정(권장값 제안)
2. 홈/일일 요약: 오늘 섭취 칼로리, 목표 대비 진행률, 최근 기록한 식사
3. 검색: 빠른 자동완성, 카테고리 필터(음식점, 브랜드, 일반)
4. 음식 상세: 서빙 사이즈, 영양성분(칼로리, 탄수화물, 단백질, 지방), 대체 서빙
5. 식사 기록: 식사 유형(아침/점심/저녁/간식), 수량 조절, 즉시 저장
6. 설정: 목표 수정, 알림, 데이터 내보내기

모바일 우선 와이어프레임 (ASCII)
- 화면 폭 기준: 375pt (iPhone X width) 권장

1) 온보딩
[Top] 큰 타이틀: "Start tracking your calories"
[Center] 입력: 목표 칼로리 자동제안 토글 + 수치 입력
[Bottom] CTA: "Start" (Primary)

2) 홈 / 일일 요약
[Header] 날짜 선택(← 날짜 →)
[Progress] 원형/막대 진행바: 1200/2000 kcal (색: primary green)
[Quick Log] + 버튼(플로팅) — 새 기록
[Feed] 오늘의 식사 리스트(아침, 점심 등) — 각 카드에 칼로리 합계

3) 검색
[Search Bar] 서치 입력 + 음성 아이콘
[Auto-suggestions] 최근 검색, 인기 항목
[Result List] 카드: 이름 / 서빙 / kcal / + 버튼

4) 음식 상세
[Header] 음식명
[Main] kcal 강조(큰 폰트)
[Details] 영양표(탄/단/지) — 서빙 변경 드롭다운
[Actions] 수량 조절 (- 1 +) / 저장(Primary)

5) 식사 기록 모달
[Sheet] 상단 드래그 핸들
[Fields] 식사 유형 선택(토글), 시간, 음식 리스트(편집 가능)
[Save] 하단 고정 Save 버튼

6) 설정
[List] 칼로리 목표, 알림, 단위(그램/온스), 데이터 내보내기

컴포넌트 스펙
- 색상
  - Primary: #0BBF7A (progress, primary buttons)
  - Accent: #1F8FFF (interactive highlights)
  - Background: #FFFFFF
  - Surface: #F6F7F9
  - Text primary: #111827
  - Text secondary: #6B7280
- 타이포그래피
  - H1: 20/28 SemiBold (앱 큰 타이틀)
  - H2: 16/22 SemiBold (섹션 제목)
  - Body: 14/20 Regular
- 버튼
  - Primary: full-width, 48pt height, radius 12, shadow subtle
  - Secondary: outline
- 카드
  - padding 12, radius 10, elevation low
- 아이콘/터치 영역
  - 아이콘 크기 24px, 최소 터치 타깃 44x44pt

상호작용(Interaction notes)
- 검색 자동완성: 입력 시작 200ms 디바운스, 서버 호출(최대 10개) → 목록 표시
- 음식 선택 → 모달로 음식 상세 표시(시각적 포커스 라이트박스)
- 저장 시 스낵바: "Saved to Lunch" (undo 3s)
- 진행바 업데이트 애니메이션: 300ms ease-out

접근성(Accessibility)
- 색상 대비: 텍스트 대비 최소 4.5:1 (본문), 버튼 텍스트 4.5:1 권장
- 화면 리더: 모든 레이블에 accessible name 제공(예: "Search foods, input")
- 큰 텍스트 지원: 시스템 폰트 크기 증가 시 레이아웃 깨지지 않음(플렉스 기반)
- 키보드 접근성: 폼 필드에 logical tab order
- 터치 타깃: 44x44pt 이상

결정 기록(Design Decisions)
- 카드 레이아웃 선택 이유: 식사 항목이 스캔 가능해야 하므로 시각적 분리 필요
- 원형 진행바 대신 가로 막대도 고려했으나, 막대는 가시적 가독성에서 유리 → 홈 화면은 가로 진행바 + 작은 원형 요약 조합 사용

Figma & 에셋 작업 지침
- Figma 파일 생성 권장 이름: "Diet Calorie App — v1 (Maya)"
- 페이지 구성: 01_Specs, 02_Wireframes_Mobile, 03_Components, 04_Exports
- Component set: Buttons, Inputs, Cards, BottomNav, ProgressBar, Modal
- Variants: 버튼 (Enabled, Disabled, Loading)
- PNG Export presets: see output/design/export_presets.md

Acceptance criteria (디자이너 관점)
- 모든 주요 스크린의 모바일 와이어프레임(위 문서 포함) 작성 완료
- 컴포넌트 토큰(색, 타이포, 버튼) 정의 완료
- Figma 파일 생성 또는 공유 지침 제공
- PNG export 규격 정의

다음 단계
- Figma 파일 생성 및 키 스크린(온보딩, 홈, 검색, 음식 상세, 식사 기록 모달, 설정) PNG 6개 업로드 필요

파일 생성: output/design/diet_calorie_app_spec.md

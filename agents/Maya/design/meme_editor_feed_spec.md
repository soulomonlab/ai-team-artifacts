# Meme Editor & Feed 디자인 스펙

요약
- 산출물: 하이파이 목업 기준의 디자인 스펙(편집기 + 피드)
- 파일: output/design/meme_editor_feed_spec.md
- 목적: upload, 텍스트 오버레이, 드래그/포지셔닝, 스타일 옵션, 피드(무한스크롤, 좋아요/댓글/공유) 구현을 위한 디자인 가이드

대상 유저 & 사용 맥락
- 대상: SNS 성격의 가볍고 빠른 밈 생성/공유를 원하는 18-35세 사용자
- 사용 맥락: 모바일 우선(대부분 사용), 데스크톱에서도 편집 가능. 짧은 작업(30s 내) 목표.

주요 결정(요약)
- 모바일 우선 설계: 편집 컨트롤을 하단 고정 바에 배치하여 엄지 사용 최적화
- 카드형 피드: 이미지 중심의 카드 레이아웃으로 시각적 우선순위 확보
- 텍스트 오버레이는 레이어 기반(포지션+스타일), 드래그로 이동, 이중 탭으로 편집
- 스타일 옵션은 ‘프리셋’ + ‘세부 조정’으로 나눠 초보자/고급자 모두 지원

User Flow
1. 홈(피드) 진입 → 무한 스크롤로 카드 로드
2. 상단 + 버튼/플로팅 FAB → 새 밈 생성(이미지 업로드/카메라/템플릿)
3. 편집 화면: 캔버스 중앙, 하단 툴바(텍스트, 스티커, 필터, 스타일, undo/redo, 저장/공유)
4. 텍스트 추가 → 편집 모드(키보드) → 완료하면 텍스트 레이어로 전환 가능
5. 텍스트 선택 → 드래그로 위치 조정, 하단에서 폰트/색/크기/정렬 옵션 노출
6. 저장/공유 → 업로드/피드로 포스트

핵심 화면(ASCII 와이어프레임)
- 모바일 편집 화면 (세로)

[ 상단: 뒤로 | 제목(편집) | 미리보기 ]
-------------------------------------
|                                   |
|            캔버스(이미지)         |
|   (텍스트 레이어/터치로 선택)    |
|                                   |
-------------------------------------
| 툴바: 텍스트  스티커  필터  스타일 |
|(프리셋) (폰트) (색상) (정렬) ...  |
-------------------------------------
| 하단 액션: 취소  저장/공유(프라이머리) |
-------------------------------------

- 데스크톱 편집 화면 (가로)
[ 사이드바(옵션) ] [ 캔버스(중앙) ] [ 속성패널(오른쪽) ]

피드 화면(모바일)
-------------------------------------
| 탐색바: 로고 | 검색 | 새 포스트(+)       |
-------------------------------------
| 카드 1: 이미지                      |
|      밈 텍스트(오버레이)            |
|      바: 좋아요 댓글 공유  작성자     |
-------------------------------------
| 카드 2: ...                         |
-------------------------------------
(무한스크롤)

컴포넌트 스펙
- Canvas
  - 동작: 이미지 렌더링, 터치/마우스로 텍스트/스티커 선택 및 이동
  - 제약: 최대 2048px 축소/확대 허용, 초기 fit-to-screen
  - 핀치 줌 지원(모바일)

- Text Layer
  - 기본 동작: 더블탭/이중탭 = 편집 모드, 단일 탭 = 선택/이동
  - 프로퍼티: content, fontFamily, fontSize(px), color(hex), stroke(boolean + color), alignment(left/center/right), shadow, rotation(deg), zIndex
  - 최소/최대 폰트 사이즈: 12px - 200px (반응형)

- Toolbar (mobile bottom)
  - 높이: 64px, 아이콘 크기 24px
  - 버튼: 텍스트, 스티커, 필터, 스타일, undo, redo, export
  - 상태: 선택된 툴 하이라이트(#FF6B6B, 2px 상단 보더)

- Feed Card
  - Width: 100% (mobile), Max-width: 720px(centred on desktop)
  - Image aspect: variable, cover behavior
  - Metadata row: avatar(40px) + author + timestamp
  - Action row: like(아이콘 + count), comment(count), share
  - Tap image → 상세 모달(확대 + 댓글)

Spacing, Grid, Typography
- Grid: 4px base spacing
- Spacing tokens: xs=4, s=8, m=16, l=24, xl=32
- Typography
  - H1: 28px / 34px line-height / 700 (desktop headline)
  - Body: 16px / 24px / 400
  - Small: 12px / 16px
  - Caption (meta): 13px
- Font family: Inter (default), fallback: system-ui, -apple-system, 'Segoe UI'

Color & Tokens
- Primary: #FF6B6B (action, primary buttons)
- Secondary: #2F80ED (links, accents)
- Neutral-900: #0B1320 (text)
- Neutral-700: #475569 (muted text)
- Surface: #FFFFFF (cards)
- Overlay (modal backdrop): rgba(11,19,32,0.6)
- Success: #22C55E, Danger: #EF4444
- Use CSS variables: --color-primary, --color-neutral-900, etc.

Responsive Breakpoints
- Mobile (default): 0 - 599px — 앱모드, 툴바 하단 고정
- Tablet: 600 - 1023px — 캔버스 비중 증가, 옵션 팝오버
- Desktop: 1024px+ — 좌/우 패널 활성화, 캔버스 중앙
- Canvas padding: mobile 12px, tablet 24px, desktop 48px

Interactions & Microcopy
- 텍스트 드래그: 즉시 따라옴 (no easing), 드래그 끝나면 snap grid 8px 단계
- 선택된 레이어에 1px stroke outline (#FF6B6B 12% alpha)
- Undo/Redo 10단계 지원
- Autosave draft: 5초 inactivity or onBlur
- 이미지 업로드: progress bar + optimistic preview

Accessibility
- Contrast ratios: ensure text over image uses adaptive stroke or contrast check (min 4.5:1 for body)
- Tap targets >= 44x44px
- Keyboard: tab to select layers, arrows to nudge 1px, shift+arrow 8px

Assets to deliver
- SVG icons: upload, text, sticker, filter, undo, redo, like, comment, share (24px + 48px variants)
- Template images: 10 starter templates (PNG/JPG) — filenames: template_01.jpg ... template_10.jpg
- Fonts: Inter variable webfont links + local fallbacks

Implementation notes / Backend expectations
- Upload API: POST /v1/uploads -> returns imageUrl, width, height
- Feed API: GET /v1/posts?pageToken=... (cursor-based) returns author, counts, imageUrl, overlay metadata
- Post API: POST /v1/posts payload includes layers array with type,text,props
- Signal needed for optimistic like toggles (toggle endpoint)

Design decisions (세부 설명)
- 모바일 하단 툴바: 이유 — 한 손 조작 최적화. 상단 툴바는 복잡성을 줄이기 위해 최소화.
- 프리셋 + 세부 조정: 초보자는 프리셋 빠른 적용, 고급자는 세부 컨트롤로 정밀 편집 가능.
- 카드형 피드: 이미지가 핵심 콘텐츠이므로 카드 레이아웃으로 가독성 확보.

Acceptance criteria for handoff
- 컴포넌트별 Storybook 스토리(혹은 샘플 페이지)로 재현 가능
- 텍스트 레이어의 드래그/편집/스타일 기능 테스트 가능한 상태
- 피드에서 무한스콜과 좋아요/댓글/공유 액션 동작

파일/아트워크 위치
- SVG 아이콘: output/design/assets/icons/
- 템플릿 이미지: output/design/assets/templates/

결론 / 다음 단계
- 개발: #ai-frontend(Kevin)에게 컴포넌트 구현 요청
- 백엔드 연동 협의: Marcus와 업로드/포스트 API 스펙 확인
- QA: 기본 시나리오 및 접근성 체크리스트 제공

문제가 되거나 제약이 있으면 즉시 피드백 주세요.

Maya (Designer)
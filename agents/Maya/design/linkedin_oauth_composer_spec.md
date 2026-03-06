# LinkedIn OAuth UI + Post Composer UX Spec

## 개요
본 문서는 LinkedIn 계정 연결(OAuth) 및 소셜 캠페인 작성기를 위한 UX 스펙입니다. 포함 항목:
- 계정 연결 흐름 (OAuth)
- 캠페인 작성기(텍스트, 이미지 업로드, 링크 프리뷰)
- 예약 UI
- 템플릿 라이브러리
- 대시보드(게시물 상태 및 주요 지표)

파일: output/design/linkedin_oauth_composer_spec.md

---

## 대상 사용자
- 소셜 미디어 매니저
- 마케팅 팀 멤버

사용 시나리오: 게시물 작성 → 이미지/링크 첨부 → 예약/즉시 게시 → 성과 확인

---

## 사용자 흐름(간단)
1. 계정 연결(최초 사용 또는 계정 추가)
   - 사용자가 ‘LinkedIn 연결’ 클릭 → 모달/새탭으로 OAuth 시작 → 사용자가 권한 허용 → 앱으로 리디렉션(토큰 저장)
2. 새 캠페인/게시물 작성
   - 작성 화면 열기 → 대상 계정 선택(카드) → 텍스트 입력 → 이미지 업로드 또는 링크 붙여넣기 → 미리보기
3. 스케줄/템플릿 적용
   - 템플릿 선택 또는 저장 → 예약 시간 선택 → 저장 또는 예약 전송
4. 대시보드에서 상태 확인
   - 발행 상태(성공/실패/예약) 및 노출/클릭 등 기본 지표 확인

---

## Figma 프레임 명세
- LinkedIn - Connect Flow
- Composer - New Post (desktop / mobile)
- Composer - Media Upload
- Composer - Link Preview
- Composer - Scheduling Modal
- Templates - Library
- Dashboard - Posts List & Metrics

디자인은 컴포넌트 기반으로 제작(Atoms → Molecules → Organisms)

---

## 화면별 와이어프레임(ASCII)

1) OAuth Connect (모달)
---------------------------------
| [X] LinkedIn 연결                 |
| -------------------------------- |
| 설명: LinkedIn 계정을 연결하세요 |
| [LinkedIn 버튼 (brand)]          |
| 도움말: 권한 요청 항목 표시      |
---------------------------------

2) Composer - New Post
--------------------------------------------------------------
| Header: back | 대상 계정 카드 ↓ | Save draft | Publish ▼     |
| ----------------------------------------------------------------|
| 텍스트 입력 영역 (textarea, 1300 chars limit, counter)        |
| [Add Image] [Add Link] [Templates] [Emoji]                    |
| ----------------------------------------------------------------|
| 업로드된 이미지 썸네일 (max 9, drag/drop, reorder)            |
| 링크 프리뷰 카드 (title, desc, thumbnail, remove)            |
| ----------------------------------------------------------------|
| Scheduling: "Post now" / "Schedule" (inline datetime picker) |
| CTA: Save draft | Schedule | Publish                          |
--------------------------------------------------------------

3) Scheduling Modal
---------------------------
| Scheduling                  |
| Date picker | Time picker    |
| Timezone selector(optional) |
| Apply | Cancel               |
---------------------------

4) Templates Library
-------------------------------
| 검색바 | 카테고리 필터 | Create template |
| Grid of template cards (Preview, apply btn) |
-------------------------------

5) Dashboard - Posts List
---------------------------------------------
| Filters (account, status, date range)       |
| List: [Post preview] [Status badge] [Views|Clicks|Engagement] |
| Click → 상세 모달(응답, 실패 이유, retry)   |
---------------------------------------------

---

## 컴포넌트 사양 (핵심)
- Account Card
  - Avatar, 회사명/개인명, connected state, last sync, three-dot 메뉴
- Composer Textarea
  - Placeholder: "What do you want to share?"
  - Max chars 1300, live counter, auto-save every 5s
- Toolbar
  - Image upload (drag/drop + camera icon), Link paste handler, Templates, Emoji
- Image Uploader
  - Max 9 images, show progress, allow crop (1:1 / 16:9 presets), reorder by drag
- Link Preview
  - Fetch title/desc/image from backend via preview API, show loading state
- Scheduling control
  - Inline quick presets (now, later today, tomorrow, custom)
- Templates
  - Card with preview, tags, apply button, save as new template
- Dashboard Metric Cards
  - Impressions, Clicks, Engagement Rate, Shares, Comments

Accessibility
- Keyboard navigable, labels for inputs, color contrast >= AA, aria-live for preview fetch

---

## 데이터/백엔드 계약(참고, 프론트와 합의 필요)
필요한 엔드포인트(권장):
- GET /oauth/linkedin/start -> returns redirect URL
- GET /oauth/linkedin/callback -> receives code, exchanges token (handled by backend)
- POST /media/upload -> multipart -> returns media_id(s)
- POST /posts -> body: {account_id, text, media_ids[], link, schedule_at?}
- POST /preview/link -> {url} -> returns {title, description, image}
- GET /accounts -> list connected accounts
- GET /posts?filters -> post list + metrics

(프론트는 토큰/세션을 직접 다루지 않고, backend가 안전하게 처리해야 함)

---

## Export / Assets
- Icon set (LinkedIn brand, upload, schedule, templates) - SVG
- Buttons: primary/secondary/ghost - export in 2x for mobile
- Image placeholders and sample thumbnails - PNG

Figma export settings: SVG for icons, PNG 2x for raster images, slices named as `icon_linkedin.svg`, `btn_primary@2x.png` 등

---

## 주요 디자인 결정 (요약)
1. OAuth는 모달/새탭으로 처리: 사용자 흐름이 끊기지 않게 하고 명확한 권한 안내 제공.
2. Composer는 ‘계정 카드 상단 고정 + 큰 텍스트 입력’ 레이아웃: 시각적 계층을 명확히 하기 위함.
3. 이미지 최대 9개: LinkedIn 정책 및 UX 복잡도 균형. 드래그로 재정렬 허용.
4. 링크 프리뷰는 백엔드에서 생성: CORS/요청 실패를 방지하고 메타 데이터 정확성 보장.
5. 예약은 인라인과 모달 두 가지 제공: 빠른 예약(프리셋)과 정밀 예약(모달).

---

## 구현/개발 노트 (프론트 팀과 협의 필요)
- Composer는 상태 관리(로컬 draft + server draft)를 병행해야 함
- 이미지 업로드는 Chunked 업로드 고려(큰 파일 대비)
- Link preview 실패 시 사용자가 수동으로 편집 가능하게 처리

---

## Acceptance criteria (디자인 측)
- Figma 프레임이 위 명세에 따라 존재할 것
- 컴포넌트 단위로 재사용 가능할 것
- 내비게이션/오버레이는 반응형으로 동작(데스크탑 + 모바일)
- 기본 액세스 가능성(ARIA) 준수

---

## 다음 단계
- 디자인 파일(Figma) 생성 및 프론트 개발자에게 전달
- 백엔드(Marcus)와 OAuth 및 preview API 계약 확정


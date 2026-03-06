# Landing Variants — Final Screens & Design Tokens

요약
- 산출물: 데스크탑+모바일 최종 화면 설계(3개 카피 버전) + 디자인 토큰(JSON)
- 파일: output/design/landing_variants_spec.md, output/design/landing_variants_tokens.json
- Figma: https://www.figma.com/file/PLACEHOLDER/Landing-Variants-Maya  (팀에 공유된 실제 파일로 교체해주세요)

목표
- GrowthContent에서 크리에이티브 제작 완료 가능하도록 최종 화면과 일관된 디자인 토큰 제공
- 추적 위치(데이터 속성)와 CTA 스타일 일관성 유지

Deliverables (간단)
1) Desktop + Mobile 화면: Variant A / Variant B / Variant C (각각 데스크탑/모바일)
2) 디자인 토큰 JSON: 색상, 타이포그래피, spacing, CTA 스타일
3) 추적 가이드: CTA & 유입 폼에 넣을 data-* 속성 지정

사용자/맥락
- 유입: 페이드/검색/광고에서 랜딩
- 목표: 폼 제출 또는 CTA 클릭(핵심 전환)
- 디바이스: 데스크탑 우선, 모바일 필수

주요 디자인 결정 (요약)
- 동일 레이아웃(헤더 → 히어로 → 기능/혜택 → 소셜증거 → CTA 폼) 유지: 재사용성 및 A/B 비교 용이
- CTA는 상단(히어로)과 중간(섹션 끝) 두 곳 배치. 히어로 CTA는 primary, 하단은 secondary
- 카드형 섹션으로 정보 계층 명확화(스크롤 스캐닝 개선)
- 접근성: color contrast WCAG AA 목표(최소 4.5:1 버튼 대비)
- 추적: 각 CTA/form에 data-track-id="variantA_hero_cta" 형태로 설정

와이어프레임 (ASCII)
- Desktop (공통 레이아웃)
  ------------------------------------------------------
  | Header [logo]            [nav]           [cta small]|
  ------------------------------------------------------
  | HERO: Left: H1 / Copy    Right: Visual/illustration |
  |       [Primary CTA] [Secondary Link]                |
  ------------------------------------------------------
  | Features (3 cols card)                                  |
  ------------------------------------------------------
  | Social proof / logos                                     |
  ------------------------------------------------------
  | Mid CTA (compact)                                        |
  ------------------------------------------------------
  | Footer                                                  |
  ------------------------------------------------------

- Mobile (stacked)
  -------------------------
  | Header [logo][menu]   |
  -------------------------
  | HERO: H1
  | visual
  | [Primary CTA]
  -------------------------
  | Features (stacked cards)
  -------------------------
  | Mid CTA
  -------------------------

컴포넌트 사양(요약)
- Header: sticky=false, height desktop=72px mobile=56px
- H1: 40/48px (mobile/desktop), weight=700
- Body copy: 16px, line-height=1.5
- Button primary: border-radius=8px, padding: 16px 24px
- Form inputs: height=48px, radius=8px, label 상단 배치

추적(Tracking) 위치 및 data attributes
- Hero primary CTA: data-track-id="{variant}_hero_cta"
- Hero secondary link: data-track-id="{variant}_hero_secondary"
- Mid-CTA: data-track-id="{variant}_mid_cta"
- Form submit: data-track-id="{variant}_form_submit"
- 각 버튼에 data-track-label 예시: "signup_hero_top" 권장

Export / Figma handoff
- Figma 파일에서 아래 이름으로 화면 내보내기 (PNG @2x)
  - variantA_desktop.png, variantA_mobile.png
  - variantB_desktop.png, variantB_mobile.png
  - variantC_desktop.png, variantC_mobile.png
- Assets: logos, illustrations -> SVG

Acceptance criteria
- 3 variants의 데스크탑+모바일 화면 PNG 또는 Figma URL 공유됨
- output/design/landing_variants_tokens.json 가 제공됨
- 추적 data-* 속성 위치가 스펙에 명시됨

Notes / To implementer's checklist
- Ensure button color contrast >=4.5:1
- Keep hero headline HTML H1 on page
- Use tokens from JSON (no hardcoded colors)

문서 끝.

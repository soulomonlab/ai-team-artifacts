# Feature: First-Time User (FTU) Guided Onboarding

**Goal:**
간편하고 안내 중심의 첫 사용 경험을 통해 신규 사용자의 제품 이해도를 높이고 핵심 기능으로의 활성화(activation) 비율을 증가시킨다.

**North Star Impact:**
신규 사용자 활성화 비율 증가 → 장기적 유지율과 전환률 개선

**Users:**
- 페르소나 A: 제품을 처음 접한 일반 사용자 — 가입 후 핵심 기능(예: 설정 완료, 첫 게시물, 첫 결제)을 빠르게 완료하고자 함
- 페르소나 B: 기술에 익숙하지만 시간 여유가 적은 사용자 — 최소 입력으로 가치 경험을 원함

**RICE Score:**
- Reach = 5,000 신규 사용자 / 분기(추정)
- Impact = 2 (Performance)
- Confidence = 70% (Taylor의 초기 수치 및 과거 유사 실험 참고)
- Effort = 3 person-weeks
- RICE = (5000 × 2 × 0.7) / 3 ≈ 2333

**Kano Category:** Performance

## Context
- 현재 FTU 경로는 선택적 도움말과 정적 튜토리얼만 제공되어, 핵심 목표(Activation)까지 사용자가 이탈하는 비율이 높음.
- Taylor(Tech Lead)가 제시한 수용 조건 및 추정치(간단한 3단계 여정, 이벤트 추적 필요)를 기반으로 PRD 작성.

## Goals
- 핵심 활성화 지표(Activation)를 10%p 향상
- FTU 중 이탈률을 15% 감소
- 30일 유지율(DAU/MAU 초기 코호트)을 5%p 개선

## User Journey (3 steps)
1) 환영 + 가치제안 (Onboarding modal / welcome screen)
   - 사용자에게 핵심 가치 1문장 전달
   - ‘시작하기’ CTA
2) 핵심 작업 가이드 (핵심 기능 1개씩, 최대 2~3개) — 인터랙티브 튜토리얼
   - 단계별 플로우: 예시 입력/샘플 데이터로 직접 시도
   - 툴팁 + 스킵 옵션
3) 완료 + 다음 행동 유도 (Success screen)
   - 완료 체크리스트, 추천 다음 행동(예: 친구 초대, 프로필 완성)
   - 간단한 리워드/배지(옵션)

## Acceptance Criteria
- [ ] 신규 가입자 중 80%가 Onboarding 첫 화면을 보도록 트리거됨
- [ ] 사용자는 언제든 Onboarding을 스킵하거나 나중에 재진행 가능
- [ ] 핵심 Activation 이벤트(정의 아래) 발생 추적이 정상 작동
- [ ] 응답성: 온보딩 모달/튜토리얼 로드 시간 < 300ms (프론트 성능 목표)
- [ ] 보안: 민감 정보 요청 없음, 권한 요청은 별도 모달에서 처리

## Activation 정의 (Success Metrics)
- Activation = 신규 사용자가 가입 후 7일 이내에 ‘핵심 기능 1개 이상 사용 AND 프로필(또는 기본 설정) 50% 이상 완료’
- Success metrics to track:
  - Activation rate (day7)
  - FTU drop-off funnel (screen-by-screen)
  - Time-to-activation (median)
  - 30/60-day retention for activated vs non-activated cohorts

## A/B Test Design
- Goal: 어떤 온보딩 플로우가 Activation을 더 잘 유도하는가
- Variants:
  A (Control): 현재 상태(경량 도움말)
  B (Full Guided): 3-step interactive guided onboarding (recommended)
  C (Light + Incentive): 2-step minimal flow + small reward
- Sample size: baseline 활성화율 20% 가정 시, 최소 검정력 80%로 각 그룹 n≈1,500 필요(정확 계산은 데이터팀과 상의)
- Key metric: day7 Activation rate (primary), time-to-activation (secondary)
- Duration: 최소 2~4주 또는 필요한 표본 도달 시 종료

## Analytics / Events Spec (high-level)
- Events to emit (각 event에 user_id, session_id, timestamp, variant):
  - onboarding.shown (screen, variant)
  - onboarding.step.start (step_number)
  - onboarding.step.complete (step_number)
  - onboarding.skipped (step_number/where)
  - activation.triggered (activation_components: [feature_used, profile_completion])
  - onboarding.completed
- Funnel: onboarding.shown → step.complete (each) → onboarding.completed → activation.triggered
- Tag properties: referral_source, device_platform, geolocation, experiment_variant
- Plan: implement high-level spec here, Taylor/Marcus to finalize event schema and ownership

## Security Considerations
- 온보딩에서 민감 데이터(결제정보, SSN 등) 절대 요청 금지
- 최소 권한 원칙: 추가 권한(푸시, 연락처 등)은 핵심 가치 전달 후 별도 명시적 동의 화면에서 요청
- 이벤트 데이터는 PII 제거/마스킹 필요(예: 이메일, 전화번호)
- 로그에 사용자의 전체 입력값이 기록되지 않도록 주의

## Rollout Plan
- Phase 0 (Internal alpha): 내부 직원 5% 트래픽 — 1주
- Phase 1 (Beta): 신규 사용자 20% — 2주, 모니터링(버그 + 핵심 지표)
- Phase 2 (Gradual): 50% — 2주
- Phase 3 (Full): 100% 롤아웃, 모니터링 2주
- Feature flags for instant rollback

## Timeline & Estimated Effort
- Discovery & final spec: 0.5w (Product)
- Design (wireframes & microcopy): 1.5w (Maya)
- Frontend implementation: 2.5w (Kevin)
- Backend/events + analytics: 1.5w (Marcus)
- QA & Beta: 1w (Dana)
- Total effort (cross-functional): ~7 weeks calendar (approx 4.5 person-weeks aggregated)

## Owners
- Product (PO): Alex (you) — PRD, acceptance, analytics success
- Design: Maya — wireframes, microcopy, accessibility
- Frontend: Kevin — component implementation, performance
- Backend/Events: Marcus — event schema, APIs, feature flag
- QA: Dana — test plan, acceptance tests

## Open Questions (for Product review)
1. Taylor이 제공한 'acceptance highlights and estimates'에 구체 수치(로드 타임, 이벤트 SLA 등)가 더 있나요? 있으면 반영 필요.
2. Activation 정의(프로필 50% 기준)는 적절한가? 제품팀 의견 필요.
3. 샘플 사이즈 및 A/B 검정 설계에서 데이터팀의 정확한 baseline 제공 필요.
4. Reward(배지/인센티브) 사용 시 마케팅/법무 검토 필요 여부

**GitHub Issue:** (생성 후 링크 삽입)

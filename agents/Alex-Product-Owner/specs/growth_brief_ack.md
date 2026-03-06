# Feature: Canonical Activation% Definition for Growth Experiments
**Goal:** 규정된 "activation%" 정의(메트릭 공식, 이벤트 목록·순서, 귀속 윈도우, 제외 규칙)를 제공해 GrowthContent의 실험 KPI·샘플사이즈 계산에 사용 가능하게 함
**North Star Impact:** 활성화 비율(activation%)의 일관된 정의로 실험 비교 가능성 확보 → 실험 우선순위와 의사결정 속도 향상
**Users:** Growth PMs, Data/Analytics 팀, Backend/Frontend 엔지니어, QA

**RICE Score:** Reach=50,000 (분기 신규 유입 추정) × Impact=1 (중간) × Confidence=80% / Effort=1w = 40,000
**Kano Category:** Must-have (Growth 실험 KPI의 공통 계약)

## Canonical activation% 정의 (권장)
- 정의 요약(한줄):  신규 유저(또는 실험의 할당 대상)가 최초 유입(예: landing visit 또는 ad click)로부터 지정된 귀속 윈도우 내에 ‘Activation Event’ 조건을 충족한 비율.

### 1) 대상(분자/분모)
- 분모 (Eligible users): 실험에 노출된 고유 사용자 수(유효한 user_id 또는 anonymous_id 기준, 중복 제거). 단, 이미 기존에 activation 조건을 충족한 기존 유저(재참여 유저)는 제외 unless experiment targets reactivation.
- 분자 (Activated users): 분모에 속한 사용자 중 귀속 윈도우 내에 아래 ‘Activation Event’ 시퀀스를 만족한 사용자 수.

### 2) Activation Event (이벤트 이름 및 순서)
- 이벤트 이름(권장 표준, analytics schema와 맞출 것):
  - page_view (landing 방문) — optional (노출판별 목적)
  - signup_completed (사용자 계정 생성) — required for signup-first funnels
  - auth_identified (user_id 결합 완료) — optional server-side enrichment
  - aha_event (제품별 핵심 행동: 예: first_project_created OR first_upload OR completed_tutorial)

- Canonical sequence (default): signup_completed → aha_event
  - 즉, activation은 사용자가 먼저 계정을 생성(signup_completed)한 뒤, 귀속 윈도우 내에 aha_event를 수행하면 성립.
  - 만약 캠페인이 비회원 전환(non-signup) 목표라면: page_view → aha_event (비회원 이벤트로 측정)으로 대체.

- Activation boolean rule (formal):
  - activated = EXISTS(event_t1 = signup_completed for user u at t_signup) AND EXISTS(event_t2 = aha_event for user u at t_aha) AND t_signup <= t_aha <= t_signup + attribution_window

### 3) Attribution window
- 기본: 7일(168시간) from signup_completed timestamp.
- 대체 권장안: 빠른 액션 상품은 7일, 복합 구매/설치 유도 상품은 14일; 실험 설계 시 명시적으로 선택.
- 귀속 정책: 첫 qualifying aha_event에 귀속(First-touch within window). 이후 이벤트는 중복 카운트하지 않음.

### 4) Exclusion rules
- Internal traffic: 회사 IP 블록, known QA/test accounts (email domains: @ourcompany.com), and users flagged as internal via internal_flag event property → exclude from denominator and numerator.
- Bots / Crawlers: user agents flagged by server-side bot detector → exclude.
- Duplicate users: multiple anonymous_id merged to same user_id — count unique user_id; if no user_id, dedupe by anonymous_id.
- Pre-activated users: users who satisfied activation prior to experiment exposure → exclude unless experiment explicitly targets reactivation.
- Incomplete instrumentation: sessions missing user_id and anonymous_id → ignore (log for data completeness checks).

### 5) Data & Tracking constraints (must-have)
- Event payload MUST include: user_id (nullable), anonymous_id, timestamp (ISO8601), event_name, experiment_id, variation_key, source (landing/medium), and properties for aha_event (e.g., project_id, file_size).
- Prefer server-side tracking for signup_completed and aha_event to avoid client-side ad blockers. If client-side used, ensure server-side dedup using anonymous_id.
- All activation events must be piped to analytics warehouse (Segment → Snowflake / Amplitude) with raw event log for reproducibility.
- Use consistent event names in the analytics schema. If schema gap exists, map frontend/backend events to canonical names before analysis.

### 6) Target lift thresholds & statistical guidance
- Default business-meaningful threshold: absolute +5 percentage points (pp).
- Minimum detectable effect (practical): +3pp may be actionable but needs larger sample; recommend pre-specifying minimum effect and computing sample size.
- Guidance: prefer absolute pp thresholds for reporting (easier for stakeholders). Also report relative lift.

### 7) Experiment platform & implementation notes
- Preferred: Optimizely (Web/Full Stack) or LaunchDarkly + server-side eventing. For analytics: Amplitude or GA4 + warehouse (Segment → Snowflake).
- Constraint: Platforms must pass experiment_id and variation_key with each activation event. If using client-side A/B, ensure reliable variation sync to analytics via server enrichment.

## Acceptance Criteria
- [ ] output/specs/growth_brief_ack.md 작성 및 Stakeholder 승인(Jessica).
- [ ] Events mapping table produced and agreed (signup_completed, aha_event) — Analytics/Backend sign-off.
- [ ] Instrumentation tasks created for backend/frontend and events flowing to warehouse (raw table) within 7 days.
- [ ] Sample size calculation for each experiment using this activation definition completed and attached to experiment PR.

## Out of Scope
- Power/sample size computation per-variant (Analytics to compute after instrumentation confirmed).
- Experiment assignment logic or feature flag implementation details (Engineering/Tech Lead scope).

## Success Metrics (post-launch)
- All 6 planned experiments report activation% using this canonical definition.
- Consistent activation% time-series across experiments (no >1pp variance due to instrumentation changes).

## GitHub Issue
- Will create issue: "Define canonical activation% metric for growth experiments" and link to this spec.

--
Prepared by: Alex (Product Owner)

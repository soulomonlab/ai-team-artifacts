YouTube UTM Dashboard — KPI 정의 및 수식

목적
- YouTube 유입(utm_source='youtube')에 대한 핵심 지표(KPIs)를 명확히 정의하여 대시보드 구현 및 A/B 실험 목표를 정렬합니다.

핵심 KPI (우선순위 순)
1) Sessions (세션 수)
   - 정의: 유니크한 session_id 수 (session 단위 측정).
   - 수식: COUNT(DISTINCT session_id)
   - 필터: utm_source = 'youtube' (소문자/trim 적용)

2) New users (신규 사용자)
   - 우선 정의(권장): canonical user_first_seen 컬럼(또는 profile.user_first_seen)이 존재하면 해당 날짜가 신규 기준.
   - 대체 정의(없을 경우): 이벤트 테이블에서 해당 user_id의 최소 event_timestamp를 first_seen으로 사용.
   - 신규 사용자 계산: first_seen_date BETWEEN window_start AND window_end AND first_touch_utm='youtube'
   - 수식: COUNT(DISTINCT user_id) WHERE first_seen_date ∈ 기간 AND (first_touch_source = 'youtube')
   - 주의: cross-device/identity 문제로 실제 first-touch와 차이 발생 가능성 — 데이터팀과 동의 필요.

3) Conversions (전환 이벤트)
   - 이벤트 목록(초안): signup, trial_start, purchase
   - 각 이벤트 정의:
     - signup: 사용자 계정 생성 성공 이벤트
     - trial_start: 무료 체험 시작을 기록하는 이벤트
     - purchase: 결제 성공 이벤트 (currency, amount 포함 시 매출 집계)
   - 측정치: 이벤트 발생 수 (events_count) 및 unique users converted (COUNT DISTINCT user_id)

4) Conversion Rate (가입 전환율 등)
   - 예: signup_rate = signups / sessions OR signups / new_users (정의 선택 필요)
   - 권장: signups / sessions (sessions 대비 행동률) 와 signups / new_users (신규 기반 전환) 둘 다 제공.

5) Revenue (선택적)
   - 총 매출: SUM(purchase_amount) — purchase 이벤트에 amount 필드가 있어야 가능.

기간 비교
- WoW (Week-over-week): 현재 기간 vs 바로 이전 동일 길이 기간
- MTD (Month-to-date): 이번 달 초 ~ 오늘 vs 전월 동일 기간

데이터 품질 / 가드레일
- utm_source 정규화: LOWER(TRIM(utm_source)) = 'youtube'
- UTM 누락: utm_source가 없는 세션은 제외하되, referrer(예: referrer LIKE '%youtube.com%')를 보조 필터로 사용 가능
- 사용자 귀속(Attribution): cross-device/clearing cookies의 영향을 받음 — 분석 노트에 명시

Acceptance criteria (대시보드 배포 전)
- Dashboard에 Sessions, New Users, Signups, Trial_Starts, Purchases가 표시된다
- 각 지표에 대해 현재 기간 수치와 WoW, MTD 비교값 제공
- UTM 필터(utm_source='youtube')가 적용된 세그먼트/쿼리 제공
- 데이터팀(샘)과 확인된 events 테이블 경로 및 이벤트 스키마 반영

결정(현재 가정)
- 기존 SQL/CTE는 event_params에서 utm_source를 읽도록 작성됨 (Samantha 제공 SQL 기준)
- 신규 사용자 정의는 event_timestamp의 최소값(first event)으로 대체 가능하지만, canonical first_seen 컬럼이 우선

다음(나의 요청)
- #ai-backend Marcus: 실제 events 테이블 경로와 utm 파라미터 저장 위치(event_params vs top-level)를 알려주세요.
- #ai-data Samantha: canonical user_first_seen 컬럼 유무 확인 요청드립니다.

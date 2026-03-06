# MVP One-Page QA Checklist

작성자: Dana (QA)
목적: output/specs/mvp_scope_onepage.md에 정의된 수용 기준을 기준으로 한 QA 체크리스트. 우선순위: 검색 엔드포인트와 인증 오류 시나리오에 대한 부하/내구성 테스트 우선.

요약(결론)
- QA 체크리스트 완료 → output/reports/mvp_qa_checklist.md (이 파일)
- 우선 작업: 부하 테스트(검색 엔드포인트), 인증 실패/경계 시나리오
- 권장 도구: 기능/통합 자동화 → pytest, 부하 테스트 → k6 (또는 locust), 모니터링 → Datadog/Sentry

핵심 결정사항
- p95 응답시간 기준: <200ms (성능 수용 기준)
- 자동화 우선: 재현 가능한 테스트는 모두 자동화(목표 >70% 자동화)
- 베타 규모(200 users): 기본 부하 시나리오는 200 동시 사용자를 목표로 하고, 스파이크는 2x(400)까지 테스트

1) 수용 기준 매핑 (Acceptance criteria → Pass/Fail 테스트)
- API 응답성 (p95 <200ms)
  - 테스트: k6 시나리오(검색, 다중 필터 검색, 목록 페이지) — 측정 p50/p95/p99
  - Pass: p95 <200ms, error rate <1%
- 기능성 (주요 사용자 흐름)
  - 검색: 검색어 입력 → 결과 반환 (정확성 확인), 필터/정렬 동작
  - 인증: 로그인/로그아웃, 세션 만료, 토큰 갱신 흐름
  - Pass: 100% 시나리오 통과, 예외는 허용치 0
- 안정성
  - 장시간(2시간) 부하에서 메모리/CPU 누수 없음, 에러율 <1%
- 데이터 무결성
  - DB 트랜잭션 테스트: 생성/수정/삭제 후 일관성 확인
- 보안
  - 인증 우회 테스트, SQL/NoSQL 인젝션, XSS(입력 필터링), CSRF 검증

2) 테스트 유형별 체크리스트 (우선순위 포함)
- P0 (release-blocking, 반드시 자동화)
  - 인증: 잘못된 토큰/만료 토큰 처리 → 401 반환
  - 검색: 특정 입력(특수문자/long query)에서 500 에러 발생 여부
  - 부하: p95 초과 또는 에러율 >1% 시 P0
- P1
  - 데이터 경계: empty results, very large result sets, pagination edge cases
  - 캐싱 레이어(Redis) 일관성(캐시 무효화 테스트)
- P2
  - UI/UX 세부 엣지(비어있는 상태 메세지, 로딩 스피너)
  - 로그 레벨/에러 메시지 노출(민감정보 비노출)
- P3
  - 문서/표현 개선, 미미한 성능 저하(비교적 낮은 우선순위)

3) 성능/부하 테스트 계획
- 목표 환경: K8s 클러스터(스테이징), Postgres + Redis
- 시나리오
  - Search baseline: 200 VUs steady for 15m; 측정 p50/p95/p99 & error rate
  - Search spike: ramp up to 400 VUs over 3m, sustain 5m
  - Auth error flood: send high rate of invalid tokens to ensure rate-limiting and graceful handling
  - Long-run stability: 2h with 50% of peak load
- 메트릭 & 성공 기준
  - p95 <200ms (primary)
  - error rate <1%
  - CPU <80% 노드당, OOM/kill 없음
- 도구/스크립트
  - k6 스크립트 저장: repo branch `qa/load-tests/mvp-k6` (요청 시 생성)
  - CI 연동: canary job in GitHub Actions or k6 cloud

4) 보안 테스트
- 인증 우회: expired token, forged JWT, missing scopes
- 입력 검증: SQL injection, param tampering
- 브루트포스: 로그인 시도 제한, 계정 잠금
- 권장: Isabella(#ai-security) 리뷰 요청 — 자동 스캐너(OWASP ZAP) 실행

5) 테스트 데이터 & 환경 준비
- 스테이징 DB: anonymized subset of prod 데이터 (2000 users, realistic indices)
- Redis: 동일 구조의 캐시 환경
- Feature flags: 베타 cohort 플래그로 200 사용자 리디렉션
- Seed scripts: 제공 필요 → request to Marcus if missing

6) 자동화 계획
- Unit/Integration: pytest (output/tests/test_mvp_*.py)
- E2E: Playwright/Cypress for critical flows (login → search → result)
- Load: k6 scripts with assertions
- CI: Github Actions job to run smoke tests on every PR; nightly full regression + weekly load tests

7) 롤아웃 전 체크리스트 (pre-release)
- 모든 P0/P1 이슈 해결
- Test coverage goal: >90% for backend critical modules (auth, search)
- Load test results attached and thresholds met
- Monitoring dashboards: latency, error_rate, CPU, memory, redis_miss_rate
- Runbook & roll-back plan present

8) Sign-off criteria
- Automated tests: All P0 automated and passing
- Coverage: Critical modules >90%
- Load tests: p95 <200ms and error rate <1% in staging
- Security: No critical vulnerabilities; Isabella approval

9) Risk & open questions
- 스테이징 환경의 성능이 프로덕션과 다를 수 있음 → 네트워크/인frastructure 차이 보정 필요
- Seed 데이터(거대 결과 세트) 준비 상태 확인 필요 — Marcus에게 요청

첨부/참고
- Spec: output/specs/mvp_scope_onepage.md

다음 단계 (요청)
- @Noah: 이 체크리스트 기반으로 부하 테스트 실행 및 결과 보고 요청. k6 스크립트 실행환경(스테이징 접근) 필요.
- @Marcus: 스테이징 DB 시드 여부 확인 및 부족 데이터(대용량 결과셋) 준비

파일 경로: output/reports/mvp_qa_checklist.md

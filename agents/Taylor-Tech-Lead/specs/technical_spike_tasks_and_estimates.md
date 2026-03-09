목표
- PRD에서 요구한 성능(중앙값 150ms, 10k RPS)을 기술적으로 검증하기 위한 스파이크 작업들 정의 및 시간/인력 추정.

요약 스파이크 목록
1) Spike 1 — Single-instance profiling
   - 목적: 단일 인스턴스(2vCPU/4GB 가정)에서 RPS 대비 latency 프로파일 확인
   - 작업: 준비(k6/artillery 스크립트), 실행(0→1000→2000 RPS ramp), 결과 분석
   - 산출물: latency vs RPS 그래프, CPU/메모리 사용량, p50/p95/p99 표
   - 소요: 2 dev-days (Marcus: backend), 0.5 dev-day (Noah: infra for temporary env)

2) Spike 2 — Full load scale test to 10k RPS
   - 목적: 전체 서비스(앱 + DB)를 대상으로 autoscale 정책 적용 후 10k RPS 달성 가능 여부 검증
   - 작업: infra setup(min=3), apply HPA rules, run distributed load tests, collect metrics
   - 산출물: scaling timeline, required peak instances, latency distribution, error rates
   - 소요: 4 dev-days (Marcus+Noah), 1 dev-day (Dana: QA to run & validate)

3) Spike 3 — DB bottleneck analysis
   - 목적: DB가 병목인지 확인, 쿼리/connection pooling 영향 파악
   - 작업: synthetic load on DB, slow-query log analysis, add read replicas if needed
   - 산출물: top slow queries, indexing recommendations, read-replica performance delta
   - 소요: 3 dev-days (Marcus+DB Admin), 1 dev-day (Noah)

4) Spike 4 — Cost simulation and ops runbook
   - 목적: 실제 비용 기반 시뮬레이션 및 운영(runbook) 작성
   - 작업: collect instance pricing, simulate hourly/monthly cost under different scaling scenarios, write runbook
   - 산출물: cost spreadsheet, ops runbook with scaling thresholds, alerting, rollback
   - 소요: 2 dev-days (Noah), 1 dev-day (Marcus)

5) Spike 5 — Resiliency & backpressure testing
   - 목적: 요청 우선순위화, queueing, and backpressure 전략 검증
   - 작업: implement test harness with prioritized requests, simulate overload
   - 산출물: degradations strategy doc, recommended queue sizes, rate-limits
   - 소요: 3 dev-days (Marcus + Dana), 1 dev-day (Noah)

총합 및 일정 제안
- 총 인력/시간: ~16 dev-days across roles. 병렬화 가능: Spike 1 & 4 start immediately; Spike 2 requires outputs from Spike1; Spike3 parallel with Spike2.
- 예상 캘린더: 3 weeks end-to-end if resources allocated as above.

우선순위 권장
- P0: Spike1 (profiling), Spike2 (full load)
- P1: Spike3 (DB), Spike4 (cost/runbook)
- P2: Spike5 (resiliency)

Acceptance Criteria for each Spike
- Clear measurable outputs (latency p50/p95/p99, instance counts, errors)
- Repro scripts + dashboards
- Recommendations (scale targets, infra changes)

의존성
- Test environment replicating production networking/DB sizes
- Access to instance pricing and current infra provider

추가 요청
- 현재 infra provider와 월 예산(상한)을 알려주세요. 인증 시스템 재사용 관련 latency 오버헤드 정보가 있으면 공유 부탁드립니다.

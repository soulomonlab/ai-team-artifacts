권장 백엔드 컴포넌트 및 스키마 변경 제안

목표: 재사용성, 확장성, 운영 용이성 보장. Product spec의 지표(중앙값 150ms @10k RPS, 예산 제약)를 기준으로 우선 도입을 권장하는 컴포넌트 목록과 영향, 간단한 스키마 변경 제안을 포함.

1) 컴포넌트 목록

- API Gateway
  - 역할: 인증 오프로드, 요청 라우팅, rate limiting, TLS 종료
  - 옵션: Kong / AWS API Gateway / Nginx+Lua
  - 이유: 인증이 외부 시스템이라면 게이트웨이에서 토큰 검증/캐싱으로 응답 지연 최소화 가능
  - 운영영향: 추가 비용, 구성 관리 필요

- Load Balancer + Autoscaling Group
  - 역할: 트래픽 분산, 인스턴스 스케일링
  - 옵션: Cloud provider autoscaling (Railway/Cloud Run/EC2 autoscaling)

- Redis (Caching + Rate Limiting)
  - 역할: 응답 캐시(주로 읽기), 분산 rate limiter, 토큰 블랙리스트
  - 운영영향: 관리형 Redis 권장(예: Upstash/RedisCloud)

- Connection Pooling + PgBouncer
  - 역할: Postgres 연결 관리
  - 이유: 많은 동시 연결 처리 시 DB 연결 폭주 방지

- Observability Stack
  - Prometheus + Grafana, OpenTelemetry tracing, Loki(로그)
  - 이유: 지연 원인 탐지, SLO 모니터링

- Message Queue (비동기 처리)
  - 역할: 긴 처리 작업(이메일, 리포트, 비동기 업데이트) 오프로드
  - 옵션: RabbitMQ / Kafka / Redis Streams

2) 스키마 변경 제안(예비)
- 접근 패턴에 따라 일부 읽기 전용 뷰/정규화 수준 완화 제안
- 핫 테이블 분리: 쓰기 빈도가 높은 테이블을 별도로 분리하여 파티셔닝
- 인덱스 제안: 복합 인덱스, partial index 사용 권장
- Audit trail 최소화: 필요 컬럼/테이블만 유지하여 행 크기 최적화

3) 운영(Runbook) 요약 — 오토스케일 이벤트
- 목적: 스케일 업/다운 이벤트 중 서비스 안정성 보장
- Trigger: 평균 CPU > 65% for 2m OR p95 latency > 300ms for 2m
- Scale Up: +2 instances, 최대 scale cap = 20 (subject to budget)
- Scale Down: -1 instance when CPU < 30% for 5m and p95 latency < 200ms
- Rollback: 신규 인스턴스가 boot 실패 3회 연속 시 롤백: reduce to previous count and alert on-call
- Incident steps: Alert 채널, runbook link, debug steps (check metrics, tail logs, promote read replica)

4) 비용/제약 고려
- 예산 타이트: prefer smaller instance types with more aggressive caching and read replicas vs large monolith instances
- Trade-offs: aggressive caching reduces CPU but increases cache cost; smaller DB instances with replication increase operational complexity

5) 개발/배포 권장사항
- Feature flags for changes affecting DB schema/behaviour
- Migrations via Alembic with backward-compatible steps
- Canary deploys for API changes

첨부: quick-checklist
- Prepare staging with identical infra topology (scaled down)
- Add auth latency measurement in every test
- Setup synthetic load generator with ramp-up profiles


이 파일은 각 스파이크를 GitHub 이슈로 생성할 때 사용할 상세 템플릿(제목, 본문, 수락 기준, 레이블)을 포함합니다. Alex가 바로 이슈 생성(또는 제가 생성)할 수 있게 구성했습니다.

---
Issue templates

1) [Epic] Performance Spikes: API + Autoscaling Validation (P1)
Title: [Epic][P1] Performance Spikes: API + Autoscaling Validation
Body:
- Background: Product spec requires median latency <=150ms at 10k RPS. Need to validate API design, autoscaling assumptions, and cost targets.
- Scope: See child tasks below (API load tests, infra simulation, cost modeling).
- Acceptance criteria: API spike results (k6/locust scripts + report), autoscale policy recommendation with cost scenarios, list of perf bottlenecks and mitigation plan.
- Labels: epic, backend, devops, P1

Child tasks (examples provided to create as separate issues):
A. [Task] API load test: create scripts + baseline measurements
- Body: Select 5 core endpoints, create k6/locust scripts, deploy to staging, run incremental load tests 1k->10k RPS, collect p50/p95/p99, error rates.
- Acceptance criteria: reproducible scripts + baseline report
- Labels: task, backend, P1

B. [Task] DB benchmark & schema validation
- Body: Collect query patterns, prepare data set, run pgbench/pgbadger, propose indexes/partitioning.
- Acceptance criteria: DB configuration proposal meeting p50/p95 targets for key queries
- Labels: task, backend, database, P1

C. [Task] Autoscale policy simulation & cost modeling
- Body: Measure single-instance RPS capacity, propose min/max and scale triggers, produce cost scenarios
- Acceptance criteria: Recommended autoscale policy + cost graphs
- Labels: task, devops, backend, P1

D. [Task] Reusable components PoC (cache, rate limiter)
- Body: Build PoC modules, integration guide, basic benchmarks
- Acceptance criteria: PoC components and docs
- Labels: task, backend, P2

E. [Task] Observability & SLO definition
- Body: Instrument endpoints with OpenTelemetry, define SLOs, create Grafana dashboards
- Acceptance criteria: Dashboards + alerting rules for p95/p99
- Labels: task, backend, devops, P1


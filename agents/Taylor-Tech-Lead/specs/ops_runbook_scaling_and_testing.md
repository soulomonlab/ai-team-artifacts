목표
- 운영팀이 오토스케일 정책을 안전하게 적용하고, 성능시험 중에 발생하는 이상 상황을 대응할 수 있도록 하는 Runbook

핵심 연락처 및 권한
- On-call: Backend (Marcus), DevOps (Noah)
- Escalation: Taylor (CTO)
- Access: load-testing accounts, dashboards (Grafana), logs (ELK/Datadog)

Pre-checklist (Before running scale test)
1. Confirm test environment mirrors production network/db sizes
2. Ensure database backups & point-in-time recovery enabled
3. Ensure feature flags to disable non-essential workloads
4. Ensure monitoring dashboards (p50/p95/p99 latencies, error rates, CPU/mem per pod, DB metrics) visible
5. Ensure alerting thresholds set for >10% error rate or p95>300ms

Run procedure
- Step 0: Announce test window to stakeholders, update runbook
- Step 1: Start with min_instances=3, confirm baseline
- Step 2: Begin ramp (e.g., 500 RPS per minute) until 10k RPS or target
- Step 3: Monitor metrics: latency, errors, DB connections
- Step 4: Observe autoscaler decisions and collect events
- Step 5: At target, hold for N minutes (recommend 5-10min) and collect traces/logs

Alert response
- If p95>500ms: pause ramp, scale up headroom manually by +50%, re-evaluate
- If error rate spikes >5%: stop test; check app logs for 5xx, DB slow queries
- If DB max connections reached: enable read-replicas or increase connection pool, use circuit-breaker

Rollback / Mitigation
- If production is blocked: revert feature flags, scale down to safe baseline (min=3) and route traffic via gateway to degraded mode

Post-test actions
- Collect artifacts: load scripts, Grafana dashboards (snapshot), autoscaler events, pod logs
- Run automated analysis script (produce p50/p95/p99 table)
- Create follow-up tasks for any observed bottlenecks

Maintenance
- Weekly smoke tests for autoscaling behavior
- Quarterly review of instance pricing & scaling thresholds

Appendix
- Recommended Grafana panels
- K6/Artillery sample ramp script snippet (stored in repo/test-infra)

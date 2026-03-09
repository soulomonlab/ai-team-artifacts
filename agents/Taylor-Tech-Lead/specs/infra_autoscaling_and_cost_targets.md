요약
- 목표: PRD 목표(중앙값 latency 150ms, 10k RPS) 충족하면서 인프라 비용/오토스케일 정책을 인프라 예산 제약 내로 맞춤.
- 산출물: 권장 오토스케일 임계값, 가정(assumptions), 비용-성능 트레이드오프, 검증 액션 플랜.

가정(명시적으로 검증 필요)
1. 애플리케이션 타입: I/O + DB 혼합. 평균 엔드투엔드 처리시간(ideal single-instance, no contention): 50-120ms.
2. 인스턴스 유형(권장 초기): 2 vCPU / 4GB RAM (컨테이너/VM). 실제 퍼포먼스는 서비스 코드/DB 호출에 크게 영향.
3. 현재 인증은 기존 시스템 재사용(추가 인증 오버헤드 최소화).
4. 네트워크/DB 지연을 포함한 환경에서 목표 중앙값 150ms 유지하려면 애플리케이션 레이어에서 p95-99 최적화 필요.

권장 스케일링 모델 (초기, 보수적)
- Horizontal pod scaling (HPA / autoscaling groups)
- 메트릭 기준: CPU(%) + custom request_concurrency (or requests/sec per pod) + queue length
- 권장 임계값:
  1) CPU target: 55-65% (보수적 안정성 확보)
  2) Request concurrency target: 목표 인스턴스당 sustained RPS = 300-600 RPS (가정범위)
     - 추천 시작값: 400 RPS per instance. (검증 스파이크로 조정)
  3) Scale down delay: 2m 이상의 안정화(avoid flapping)
  4) Scale up cooldown: immediate but enforce step limits (max +50% per minute)
- Min/Max 인스턴스:
  - Min: 3 인스턴스 (high availability & buffer)
  - Max: budget-constrained — 권장 초기 Max: 30 인스턴스. (검증 후 조정)

비용-성능 추정(예상 모델, 검증 필요)
- 가정: 400 RPS/인스턴스 → 10k RPS 요구 시 평균 동시 인스턴스 = 25 (10,000/400)
- 안전버퍼 포함: 25 → 30 인스턴스 (헤드룸 포함)
- 비용 영향: 인스턴스 단가 확인 필요(클라우드/hosted). 비용 목표를 "월간 단가 기준 예산 한도"로 명시해 주세요. 현재 예산 제약이 있으면 Max 인스턴스 수를 그에 맞춰 조정.

권장 정책 (비용 제약 반영)
- 비용 우선 시나리오: Max 인스턴스 낮춤(예: 12~15), 대신 큐잉/GRPC 스트리밍, 백프레셔 적용 및 요청 우선순위화.
- 성능 우선 시나리오: Max 인스턴스 30+, 빠른 scale-up, 더 넓은 p95 SLA.

단계별 검증 액션
1. Spike A — 인스턴스 용량 프로파일링: 단일 인스턴스(2vCPU/4GB)에서 RPS별 latency 곡선 측정 (0→1000→2000 RPS)
2. Spike B — 전체 시스템 10k RPS 시나리오: 시작 Min=3, scale rules 적용 후 필요한 Max 인스턴스 측정
3. Spike C — 비용 모델링: 실제 인스턴스 가격을 적용한 월간/시간당 비용 시뮬레이션

검증 산출물(각 스파이크마다)
- ramp-up 스크립트(artillery/k6), 결과 대시보드(throughput, latency P50/P95/P99, errors)
- Autoscaler event logs + scaling timeline
- Cost simulation spreadsheet

리스크 및 완화책
- DB 계층이 병목일 경우 인스턴스 추가만으로 해결 불가 → 캐싱, read-replica, 쿼리 최적화 필요
- 갑작스러운 트래픽 버스트 → 예열 인스턴스(Provisioned capacity) 고려

다음 단계(요청사항)
- 클라우드 인스턴스 단가(시간/월)와 현재 infra provider(예: AWS/GCP/Railway) 정보를 제공해 주세요. 비용 목표(월 예산)를 알려주시면 Max 인스턴스와 스케일 정책을 세부 조정하겠습니다.

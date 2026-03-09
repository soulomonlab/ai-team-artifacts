# Backend Architecture Proposal & CI/CD Plan

참조: output/specs/project_kickoff.md
작성자: Marcus (Senior Backend Engineer)
우선순위: P0 (Task #36)

---

요약 결론
- 제안 산출물: 고수준 백엔드 아키텍처(서비스 분해, 무상태 서비스 원칙, 캐싱, DB 파티셔닝/샤딩 옵션, 자동확장 전략, 장애 모드 및 대응)와 CI/CD 파이프라인(린팅, 유닛/통합 테스트, 커버리지 목표, 배포 흐름).
- 권장 스택(프로젝트 제약 반영): Python(FastAPI) + SQLAlchemy + PostgreSQL + Alembic, Redis(캐시/작업 큐보조), Celery(비동기 작업), Docker/Kubernetes, OpenTelemetry(분산추적).
- Acceptance criteria: 아키텍처 결정서와 CI 파이프라인 정의가 만들어져서 QA가 테스트 계획을 작성할 수 있어야 함.

---

목표(문제 정의)
- 직관적인 사용자 경험 보장
- 백엔드 확장성(트래픽 급증, 멀티-테넌트 가능성)
- 높은 코드 품질과 배포 안전성

MECE 분해
1) 서비스 설계 및 분해
2) 상태관리 및 캐싱 전략
3) 데이터베이스 확장(읽기/쓰기 분리, 파티셔닝, 샤딩) 옵션
4) 오토스케일/인프라 전략 및 장애 대응
5) 모니터링/오브저버빌리티/로깅
6) CI/CD 파이프라인과 테스트 전략

---

1) 서비스 분해(권장)
- 엣지(공통) 레이어
  - API Gateway (Ingress): 인증/권한, 라우팅, 기본 rate limiting, 리턴 포맷 표준화
- 마이크로서비스(도메인별 또는 기능별 분해)
  - Auth Service: JWT 발급/갱신, OAuth 연결, RBAC 테이블
  - User/Profile Service
  - Core Business Services (예: Items, Orders, Payments) — 각 서비스는 독립 배포 가능
  - Notifications Service (메일/푸시)
  - Background Worker Cluster (Celery) — 비동기 작업, 리트라이 정책
  - ML/Inference Service (필요 시 분리)
- 장점: 수평 확장, 팀별 소유권, 장애 격리. 단점: 운영 복잡도 증가 → 초기에는 기능별 모놀리식에서 영역별로 점진 분리 권장.

2) 무상태 서비스 원칙
- 모든 API 서버는 무상태로 설계(세션: JWT+Refresh token 사용)
- 상태 저장: Redis(세션/캐시/락), PostgreSQL(영속성)
- 비동기 처리: Celery + Redis/RabbitMQ
- 세션 및 파일 저장: S3/오브젝트 스토어 사용

3) 캐싱 전략
- 레이어:
  - CDN(Level 0) — 정적 자원
  - 애플리케이션 레벨(Level 1) — Redis 캐시(자주 조회되는 리소스, rate limit 카운터)
  - DB 쿼리 결과 캐시(캐시 어사이드 패턴 권장, TTL, 캐시 무효화 정책 정의)
- 캐시 전략 세부사항:
  - TTL 기본 5분(읽기 성능 개선), 핫키(특정 키) 모니터링 및 샤딩
  - 캐시 일관성: 쓰기 후 관련 캐시 무효화(이벤트 기반 무효화 권장)
  - 캐시 히트/미스 메트릭 수집

4) DB 확장 옵션
- 1차: 단일 PostgreSQL 마스터 + 읽기 전용 리플리카(수평 확장 비용/운영 간단)
- 파티셔닝:
  - 논리적 파티셔닝(tenant_id 또는 날짜 기반 파티셔닝)
  - 물리적 파티셔닝(분할된 DB 인스턴스) — 대규모(테라바이트) 데이터 예상 시 권장
- 샤딩 전략(트래픽/데이터가 매우 큰 경우):
  - 애플리케이션 레벨 샤딩(consistent hashing 또는 tenant -> shard map)
  - 미들웨어/DB 레벨 샤딩 솔루션 고려(예: Citus for Postgres)
- 트랜잭션/일관성: 크로스-샤드 트랜잭션 최소화. 장기적으로 CQRS 사용 검토.

5) 자동확장(Autoscaling) 전략
- 플랫폼: Kubernetes on cloud (GKE/EKS/AKS 권장)
- 수평 스케일링:
  - K8s HPA: CPU/메모리 + 사용자 정의 매트릭(큐 길이: Celery/Redis) 기반 스케일링
  - Cluster Autoscaler로 노드 자동 추가/제거
- 팟 가용성: PodDisruptionBudget, Readiness/Liveness probes
- 배포 전략: Canary(트래픽 샘플링) → 점진적 롤아웃; 롤백 자동화
- 비용 절감: 스케줄 기반 스케일링(야간 축소), 리소스 요청/한계(right-sizing)

6) 장애모드(Failure Modes) 및 대응
- DB 마스터 장애: 자동 페일오버(推荐 Patroni + PgBouncer), 읽기 장애 대비 리드 리플리카 승격 절차 문서화
- 네트워크 분리: 리전/존 레벨 복제, 장애시 트래픽 리라우팅
- 캐시 실패: degredation mode — 캐시 장애 시 DB로 폴백(읽기 성능 저하 허용)
- 서비스 폭주(Thundering Herd): rate limiting + circuit breaker + bulkhead pattern
- 작업 큐(Worker) 폭주: 큐 백프레셔, 작업 거부 정책, 모니터링 및 알람
- 부하 테스트 정례화(chaos engineering 권장)

7) 관찰성(Observability)
- Distributed Tracing: OpenTelemetry instrument 모든 신규 서비스 엔드포인트
- Metrics: Prometheus → Grafana 대시보드(요청 지연, 오류율, DB 쿼리 지연, 캐시 히트율)
- 로그: 구조화(ELK/Opensearch 또는 Loki) + 요청 ID 연계
- 알람: SLO 기반(alert on SLO breaches) + PagerDuty 연동

---

CI/CD 파이프라인 개요
목표: 빠른 피드백 루프, 높은 코드 품질, 안전한 배포

1) 파이프라인 단계(모든 merge request)
- Pre-commit hooks (ruff, isort, black 설정 권장)
- Linting: ruff/flake8, type-check(Optional: mypy for critical modules)
- Unit tests: pytest (모든 PR에서 실행) — 병렬 실행(pytest-xdist)
- Integration tests: 컨테이너 기반 통합 테스트 (Postgres/Redis test-containers or Docker Compose), 필요시 staged 환경에서 실행
- Coverage: 최소 Gate = 80% (모듈별 예외 처리 문서화). 커버리지 리포트 자동 업로드
- Security Scans: dependency scanning (safety, pip-audit), SAST (bandit)
- Build: Docker image build + image scan
- Deploy to staging: 자동(머지 시)
- E2E/Smoke tests on staging: Canary on production for critical services
- Deploy to production: Canary → 100% (자동 또는 수동 승인 옵션 선택)

2) 브랜치 전략
- trunk-based development 권장: short-lived feature branches → PR → CI 통과 후 main에 머지
- 보호된 브랜치: main에 직접 push 금지, 리뷰와 CI 성공 필요

3) 테스트 전략 및 메트릭
- Unit vs Integration 구분 명확화
- Acceptance criteria for QA: 시나리오 기반 테스트 케이스 목록
- Coverage threshold: 80% (전체) / 마이너 모듈은 70% 허용(문서화 필요)
- Test flakiness handling: flaky tests 레이블링, 데일리 재검토

4) 배포 및 롤백
- 이미지 태깅: semantic versioning + commit sha
- Canary % 설정(예: 10% 트래픽 10분 → 모니터 → 50% → 100%)
- 자동 롤백 트리거: error rate 증가(X% 초과) 또는 latency SLO breach
- 롤백 전략 문서화 (git revert 와 image 재배포)

5) 인프라/Secrets 관리
- IaC: Terraform (권장)으로 infra 관리
- Secrets: Vault 또는 cloud provider secret manager
- CD 권한 분리: 승인 워크플로(특히 prod 변경)

6) 개발자 경험 및 생산성
- PR 템플릿 (What/How to test/Risk/Rollback/Closes)
- 로컬 개발: Docker Compose + dev db fixtures
- Fast feedback: 한 PR 당 최대 실행 시간 목표 <15분 (unit+lint)

---

의사결정 요약 및 권장순서(단계별 실행)
1. 단기(0-3주): 단일 DB(마스터+리플리카), 애플리케이션 무상태화, Redis 캐시 도입, CI 기본 파이프라인(린트/유닛/커버리지)
2. 중기(3-12주): K8s 배포, HPA 설정, 오브저버빌리티 도입(OpenTelemetry + Prometheus), 통합테스트 자동화
3. 장기(3-12개월): 파티셔닝 또는 Citus 검토(데이터 성장 시), 샤딩 전략 수립, Chaos 테스트 및 SLO 운영

Trade-offs
- 마이크로서비스 분해는 확장성과 소유권을 주지만 운영 비용 증가. 초기에는 모듈화된 모놀리식 → 서비스 분해 권장.
- 샤딩은 성능을 크게 향상시키지만 개발 복잡도와 운영 비용이 증가함.

---

Acceptance Criteria (Task #36 완료 조건)
- 이 문서가 승인되어 아키텍처 원칙을 확정한다.
- CI/CD 파이프라인 설계가 QA에 인계되어 테스트 계획(통합/E2E 포함)을 작성할 수 있다.
- 다음 단계(테스트 케이스, IaC 템플릿)는 QA/DevOps와 협업해 세부화된다.

---

참고(참조 파일)
- output/specs/project_kickoff.md

---

다음 액션(내부)
- 본 문서 승인 후 세부 기술 스펙(예: DB 인덱스 전략, HPA 매트릭 설정, Terraform 모듈)를 작성.


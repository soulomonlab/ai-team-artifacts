목표
- PRD 요구사항(UX 직관성, 중앙값 150ms 목표, 10k RPS)에 맞춘 재사용 가능한 백엔드 컴포넌트 추천 및 필요한 DB/스키마 변경 제안.

핵심 권장 컴포넌트
1) API Gateway / Edge layer
   - 역할: 인증 라우팅(현재 인증 재사용), 라우팅, rate-limiting, TLS termination
   - 기술 옵션: Cloud Provider LB + Cloudflare/NGINX + rate-limit
   - 이유: 중앙 집중형 라우팅으로 레이트 리미트, WAF, TLS offloading 가능 -> 앱 서버 부담 감소

2) Service mesh (선택적)
   - 역할: 서비스간 통신 관찰성, retry, circuit-breaking
   - 기술 옵션: Linkerd (경량), Istio (완전 기능)
   - 이유: 대규모 트래픽에서 안정성 개선, 트래픽 쉐이핑 가능

3) Shared middleware: request metrics, tracing, auth hooks
   - 역할: 표준화된 tracing (OpenTelemetry), metrics (Prometheus), structured logging
   - 이유: 성능 문제 디버깅 및 SLA 보장에 필수

4) Caching layer
   - 역할: 응답 또는 DB read 캐시(예: Redis)로 p95 개선
   - 정책: TTL, cache-key 전략, 캐시 무효화 규칙

5) Connection pooling & DB replica setup
   - 역할: connection pool tuning, read-replicas for scaling reads
   - 기술: PgBouncer, Postgres replicas

6) Background worker queue
   - 역할: 비동기화 가능한 작업(offload heavy ops to background), rate-limited processing
   - 기술: Redis Streams, RabbitMQ, or Celery w/ Redis

7) Feature flagging / config service
   - 역할: runtime toggles for quick rollbacks during scale tests

권장 아키텍처 패턴
- Statless app servers behind autoscaler
- Read replicas + caching for DB-heavy reads
- Circuit breakers + retry policies for external dependencies

DB 스키마/데이터 모델 제안(조정 필요)
- 목표: 단순화, 인덱스 최적화, 읽기 중심 엔드포인트에 대한 denormalization 고려

1) Use case: user-facing listing (hot path)
   - Table: items
     - id (PK), owner_id (FK), title, summary, cached_display_json (jsonb), last_updated_at, status, popularity_score
   - 인덱스:
     - btree on (status, last_updated_at)
     - GIN on (cached_display_json) if querying within json
   - rationale: denormalized cached_display_json to reduce JOINs on hot-path reads

2) Audit/logging events
   - Table: events (append-only), partitioned by month, index on (entity_id, created_at)
   - rationale: avoid bloat on main tables, cheap append for analytics

3) Rate-limiting storage
   - Table or Redis-based counters for per-user or per-api-key limits

Migration considerations
- Backfill denormalized fields in offline job
- Add indexes gradually via low-impact migrations (pg_repack or concurrently for Postgres)

Backward compatibility
- Keep API contract stable. New denormalized fields are additive.

Acceptance criteria for schema changes
- Benchmark read latency improvement (p95 reduction) in Spike tests
- Migrations using zero-downtime patterns

Risks & Mitigations
- Denormalization increases write complexity → use background jobs, eventual consistency guarantees
- Extra caching may cause stale reads → TTL and invalidation hooks

Deliverables to produce next
- Concrete migration plan for any proposed schema changes
- Implementation templates for shared middleware (OpenTelemetry init, Prometheus metrics)


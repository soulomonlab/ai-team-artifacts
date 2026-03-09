# Model Logging Service Design

요약
- 목적: 모델 입력/출력, 예측 메타데이터, 데이터 버전, 사용자 컨텍스트를 안전하게 수집·보관하여 감사, 모니터링, 규정준수를 지원.
- 범위: 온라인/배치 추론 로그, retraining data sample, 모델 성능 메트릭, drift signals.

아키텍처 개요
1. Instrumentation (앱/모델 레이어)
   - 각 추론 요청 시 로그 이벤트 생성: request_id, timestamp, model_id+version, input_hash, output, probability/confidence, user_id (식별자 마스킹 정책 적용), raw_input 참조 링크(원본 저장소의 객체 경로)
   - 이벤트 비동기 전송: buffered queue (Kafka 또는 Pub/Sub)로 송신.

2. Ingestion
   - Consumer 서비스 (可수평확장)로 Kafka/PubSub에서 수신.
   - Validate schema (JSON Schema) → enrich (env, request headers, trace id) → redact PII → sign record (HMAC with key from Vault).

3. Storage
   - Hot store (검색용): Time-series DB / Elasticsearch / ClickHouse에 요약 레코드(메타 + pointers).
   - Cold store (원본/대형 페이로드): 암호화된 객체 스토리지(S3), 객체명에 버전·시계열 포함.
   - Audit archive: 주기적으로 cold store에서 immutable archive (WORM)로 복사.

4. Access & Query API
   - RBAC-protected REST API: 검색, 페이징, 필터(모델, 시간범위, user_id hashed, score thresholds).
   - Audit log streaming for compliance exports (CSV/Parquet) with signed manifests.

5. Retention & Privacy
   - 기본 retention: 원본 90일, 요약 2년 (조직 규정에 맞춰 조정).
   - PII 제거/마스킹 정책: 데이터 분류에 따른 자동 마스킹. 전부 보관해야 하는 경우에는 Legal+Privacy 승인이 필요.
   - 사용자 요청(삭제/포기)은 로그 인덱스에 erase marker 추가, cold store에서 해당 객체 암호화 키 폐기(비가역 삭제 절차).

6. Security Controls
   - In transit: TLS 1.2+ mandatory.
   - At rest: Server-side AES-256 encryption for S3; DB-level TDE or column encryption for sensitive fields.
   - Key management: Vault for HMAC signing keys and DEKs; CMK in cloud KMS for wrapping.
   - Integrity: Each ingestion record signed with HMAC; persistent manifest with signatures to detect tampering.
   - Audit trail: Who/when accessed logs (access logs), immutability for compliance windows.

7. Observability & Alerts
   - Metrics: ingestion rate, schema validation failures, PII redact rate, failed signs.
   - Alerts: sudden drop/increase in ingestion, abnormal distribution shift detector (model drift), data schema changes.

8. Schema (proposal)
- event_id: uuid
- timestamp: ISO8601
- model_id: string
- model_version: string
- request_id: string
- input_summary: object (hash, features_meta, pointer_to_raw)
- output_summary: object (prediction, confidence, top_k, pointers)
- metadata: {env, route, client_id}
- pii_flags: [fields]
- hmac_signature: string

Compliance & GDPR notes
- 데이터 최소화: 보관하는 raw input은 가능한 작은 샘플로 제한.
- 개인의 요청 시 지우기/익명화 프로세스 정의.
- 데이터 목적명시 및 보관기간 정책 문서화.

Implementation recommendations (reversible, incremental)
- Phase 1 (MVP): lightweight ingestion consumer + hot store summary + HTML audit dashboard prototype. No raw input by default; store pointers.
- Phase 2: full cold store, HMAC signing, retention automation, RBAC enforcement.
- Phase 3: WORM archives, third-party audit readiness, SIEM integration.

Acceptance criteria
- Ingestion API + consumer can accept test events and persist summary to hot store.
- PII fields are detected and masked in sample runs.
- HMAC signature present on persisted records.
- Audit dashboard prototype can query and render sample events.

참고
- OWASP, GDPR, NIST CSF 지침을 적용. Vault/KMS 사용 권장.

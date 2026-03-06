# Visual Inspection App — Backend Technical Specification (MVP)

Owner: Marcus (Backend)
Date: 2026-03-06
Related: GitHub Issue #112, Task #190

---

Executive summary
- Deliverable: Backend tech spec for Visual Inspection App MVP covering API surface, DB schema, ingestion architecture (edge vs cloud), queueing, storage, observability, security, effort estimates, and blocking decisions.
- Recommendation (MVP): Hybrid edge-cloud ingestion with presigned S3 uploads, Postgres for metadata, S3 for images, Redis+Celery for task queue & cache. JWT-based auth and OpenTelemetry tracing.

Goals and constraints
- P95 API latency target < 100ms; DB query < 20ms
- Image ingestion throughput expected: initially 5–20 images/min per factory line (configurable). For scaling, design for burst up to 200 images/min per line.
- Minimize bandwidth from factory floor → prefer edge preprocessing (resize, basic QC).
- MVP budget & time constraints: avoid introducing Kafka or heavy infra unless required (can be swapped later).

1) API design (v1)
Auth: Bearer JWT (access token 15m, refresh 7d with rotation). RBAC: roles {admin, operator, viewer}.
Idempotency: all mutation endpoints accept Idempotency-Key header.
Rate limiting: per-API key 100 req/min default (adjustable per client).

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST   | /api/v1/inspections | Create inspection job (metadata) | Bearer |
| POST   | /api/v1/inspections/:id/images/presign | Request presigned S3 URL for image upload | Bearer |
| POST   | /api/v1/ingest/callback | Ingestion worker callback when image uploaded & queued | Internal HMAC |
| GET    | /api/v1/inspections | List inspections (filter by device, status, time) | Bearer |
| GET    | /api/v1/inspections/:id | Get inspection metadata + result summary | Bearer |
| GET    | /api/v1/images/:id | Get signed URL / metadata for image | Bearer |
| GET    | /api/v1/results/:id | Get detailed inference result | Bearer |
| POST   | /api/v1/webhooks | Register webhook for async results | Bearer |
| GET    | /api/v1/health | Service health & readiness | None (internal)
| GET    | /api/v1/metrics | Prometheus metrics | Internal (mTLS)

API notes
- Image uploads happen directly to S3 using presigned PUTs. After upload, the uploader calls /api/v1/ingest/callback (or S3 event + queued processor) to enqueue processing.
- Alternative: provide multipart upload support for very large images but avoid for MVP.
- For UI: frontend obtains presigned URL, uploads image, then calls CreateInspection (or vice versa). Recommend flow: CreateInspection -> presign -> upload -> confirm ingestion.

2) DB schema (Postgres)
Core tables (columns abbreviated):
- devices
  - id (uuid PK), name, line_id, location, last_seen, metadata JSONB
  - indexes: pk(id), idx_devices_line

- inspections
  - id (uuid PK), device_id (fk devices), status (enum: pending, processing, done, failed), created_at, started_at, finished_at, metadata JSONB, model_version
  - indexes: idx_inspections_device_created_at, idx_inspections_status

- images
  - id (uuid PK), inspection_id (fk), s3_key, size_bytes, width, height, checksum, uploaded_at
  - indexes: idx_images_inspection_id

- results
  - id (uuid PK), inspection_id (fk), inference JSONB, anomalies_count, confidence_score, processed_at
  - indexes: idx_results_inspection_id

- webhooks
  - id, url, secret_hash, events JSONB, enabled

- users, roles, api_keys (standard auth tables)

Decisions
- Keep large binary objects out of Postgres; store only metadata and S3 key.
- Use JSONB for flexible inference payloads (model output) with GIN index on common query paths if needed.

3) Ingestion architecture: Edge vs Cloud
Options
- Cloud-only ingestion: devices upload raw images directly to cloud S3 / API. Simpler but uses more bandwidth and increases latency.
- Edge-assisted ingestion (recommended MVP): lightweight edge agent/gateway (Docker or small binary on edge box) performs:
  - local preprocessing: resize, compress, basic blur/noise QC
  - local buffering and retry (when network down)
  - upload via presigned S3 URLs or push to edge gateway which forwards to cloud ingestion API

Why edge-first for factories
- Factory networks often have bandwidth limits and intermittent connectivity.
- Edge reduces data volume sent to cloud, preserves fidelity of important frames, and allows immediate local fallbacks.

MVP choice: implement cloud ingestion API + an edge-agent spec. Edge agent is not implemented in MVP but spec + SDK snippets provided so factories can deploy. This keeps server side simple but supports edge later.

4) Queueing & processing
Options: Redis+Celery (MVP), RabbitMQ, Kafka (scale/streaming)
Recommendation: Redis broker + Celery workers for MVP. Reason: quicker to implement, good operational experience, sufficient for expected throughput. If future needs require event streaming and at-least-once semantics with complex consumer groups, migrate to Kafka.

Processing flow (MVP)
1. Client uploads image to S3 via presigned URL.
2. Client calls POST /ingest/callback with s3_key, checksum, metadata.
3. Server validates callback (HMAC or signed token), creates inspection & image records, enqueues Celery task process_image(inspect_id, image_id).
4. Celery worker downloads image from S3, runs model inference (or calls ML service), stores results in results table, updates inspection status, triggers webhooks.

Task reliability
- Celery tasks with at-least-once. Tasks must be idempotent: check if result already exists for image_id before processing.
- Retry strategy: exponential backoff, max_retries=5 for transient errors.

5) Storage choices
- Object storage: AWS S3 (or S3-compatible like MinIO). Use lifecycle policy: move to infrequent access after 7 days, expire after configurable retention (e.g., 90 days) for MVP.
- Postgres (managed, e.g., RDS/Aurora) for metadata and transactional operations
- Redis for Celery broker + caching
- Optional: Blob scanning/antivirus for security

6) Security
- Auth: JWT (15m) + refresh tokens (7d) with rotation. Use HTTPS everywhere.
- Presigned URLs limited: short TTL (5–10 min) and object path namespace per tenant.
- Ingest callback protected by HMAC signed with key derived from API key or via internal service token (short-lived).
- RBAC enforced server-side on all endpoints.
- Network: restrict metrics and admin endpoints to internal VPC. Use mTLS for service-to-service where possible.

7) Observability
- OpenTelemetry traces on API and worker tasks. Add spans for S3 upload detection -> queue enqueue -> worker processing -> model call.
- Prometheus metrics for request latencies, queue length, worker success/fail rates.
- Log structured JSON with correlation_id (generate in API and pass to workers via task headers).

8) Operational considerations
- Backpressure: monitor Redis queue length; throttle presigned URL issuance if queue > threshold.
- Monitoring alerts: worker failure rate > 1% for 5 min, queue length > N, S3 errors rate spike.
- Scaling: Celery workers autoscale based on queue length and CPU; resize Postgres read-replicas for heavy metadata reads.

9) Effort estimates (MVP) — rough (engineering days per role: BE = backend days)
Assumptions: team: 1 BE (Marcus), 1 FE (Kevin), 1 DevOps (Noah), 1 Designer (Maya)

- Design & spec (this doc): 1 day (done)
- DB schema + Alembic migrations: 1.5 days
- Core API (inspections, presign, ingest callback, results endpoints) + validation: 4 days
- Auth and RBAC (JWT, roles, API keys): 1.5 days
- Celery worker & tasks (process_image skeleton + idempotency): 3 days
- S3 integration & lifecycle config, presigned URL logic: 1 day
- OpenTelemetry + Prometheus metrics: 1.5 days
- Tests: unit + integration tests for endpoints and worker: 2.5 days
- Docker + local dev compose + sample edge-agent spec: 1.5 days
- Security review & fixes: 1 day
- Deployment + IaC (k8s manifests, Helm, CI): 3 days (Noah lead)

Total backend engineering effort (approx): 16.5 BE days (~3.5 weeks for single BE FTE). With parallel work (DevOps + FE), overall MVP backlog completion estimate: 3–4 weeks.

10) Risks & blocking decisions
- Queue choice: if expected throughput grows > 1k images/min, migrate to Kafka. For MVP Redis+Celery is fine.
- Edge agent deployment details: need confirmation on available hardware, OS, and network constraints at factories.
- Image retention & legal/compliance requirements (privacy) — confirm retention period and allowed regions for storage.
- Model serving: this spec assumes model inference happens in worker or via internal ML service. Need decision: embed inference in worker (simpler) vs call external model service (better separation). For MVP prefer worker-local call to existing model binary or container.

11) Acceptance criteria (QA)
- CreateInspection + presign + upload + callback end-to-end results in results row within 30s for typical image sizes.
- API p95 latency < 100ms for metadata endpoints.
- End-to-end successful retries for temporary S3 failures.
- Test coverage for critical paths >= 80%.

12) Next steps (for frontend & QA)
- Frontend (Kevin): implement CreateInspection + presign upload flow. Use short TTL presigned PUTs. Poll GET /inspections/:id or subscribe via webhooks for results. Confirm preferred UI UX for upload progress & retry.
- QA (Dana): prepare tests for empty payloads, duplicate callbacks, large images, network failure simulation.
- DevOps (Noah): prepare S3 bucket, Postgres RDS, Redis, and CI integration.

13) Files created
- This spec: output/specs/visual_inspection_backend_spec.md

Contact/Owner: Marcus (#ai-backend)


Appendix A — Example JSONs
- CreateInspection request
{
  "device_id": "uuid-1234",
  "metadata": {"line": "A", "shift": "night"}
}

- Presign response
{
  "upload_url": "https://s3...",
  "fields": {...},
  "expires_in": 600
}

- Ingest callback body
{
  "s3_key": "tenant/lineA/2026-03-06/uuid.jpg",
  "checksum": "sha256:...",
  "size": 123456,
  "metadata": {"frame_time": "2026-03-06T12:00:00Z"}
}

# Visual Inspection App — Technical Architecture (MVP)

Last updated: 2026-03-06
Owner: Marcus (Backend Engineer)

## Executive summary
- Deliverable: Technical architecture for Visual Inspection App MVP covering APIs, DB schema, model-serving options (cloud vs edge), scaling plan (Kubernetes + GPU strategy), monitoring, and a high-level infra cost estimate.
- Recommendation (short): Use a hybrid approach for model serving — cloud-hosted GPU-backed inference for initial MVP (managed Kubernetes with GPU node pools) and design the system to optionally support edge deployment later. Implement REST gRPC-compatible inference service behind an API gateway; store artifacts/frames in S3; metadata & annotations in PostgreSQL; Redis for caching and Celery for background jobs. Observability: OpenTelemetry + Prometheus + Grafana + centralized logs (ELK or managed alternative).

## Assumptions
- Target traffic for MVP: 50 concurrent camera streams, average 1 fps per stream (50 inference/sec) with occasional spikes to 200/sec.
- Models: 1–2 vision models (object detection + classification), ~200–600ms inference latency on a single GPU (varies by model).
- Budget sensitivity: MVP should be cost-conscious but allow burst capacity.

## High-level architecture
- Client (browser/mobile) <-> Frontend (static app, served via CDN)
- Frontend communicates with Backend API (FastAPI) for: session/annotation management, dashboard, retrieving inference overlays
- Camera ingest path: cameras push frames to an ingestion API or directly to pre-signed S3 upload endpoints
- Ingestion triggers background job (Celery/RabbitMQ) to enqueue frame for inference
- Inference workers (k8s pods, GPU-backed) pull frames from queue, run model, write inference results to DB and annotated overlays to S3
- Real-time overlay: websocket/Server-Sent Events or polling from backend to frontend to display inference overlays
- Storage: S3 for raw frames, overlays; PostgreSQL for metadata, annotations, audit; Redis for caching & rate limiting
- Auth: JWT access/refresh (15m/7d) and RBAC (roles: admin, inspector, viewer)
- Observability: OpenTelemetry traces across API + inference service, Prometheus metrics, Grafana dashboards, centralized logs

## API surface (MVP)
Auth: Bearer JWT (Access token 15m, Refresh 7d)

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /api/v1/ingest/presign | Get presigned S3 URL for uploading frame | Bearer |
| POST | /api/v1/ingest/frame | Notify server a frame is available (s3_key, camera_id, ts) | Bearer |
| POST | /api/v1/inference/trigger | (internal) enqueue inference job | Internal token |
| GET  | /api/v1/streams/:camera_id/overlay | Get latest overlay for camera (or since timestamp) | Bearer |
| GET  | /api/v1/annotations | List annotations (filter by camera, time, label) | Bearer |
| POST | /api/v1/annotations | Create annotation (bounding box, label, user_id) | Bearer |
| GET  | /api/v1/dashboard/summary | Aggregated metrics for dashboard | Bearer |
| WS/ SSE | /api/v1/streams/:camera_id/subscribe | Real-time overlay updates | Bearer |

API notes:
- Use pagination for list endpoints (cursor-based where possible)
- Standard error format: {"code": "string", "message": "string", "details": {}}
- Rate limit: per API key / per user via Redis (configurable)

## Database schema (core tables)
- cameras (id PK, name, location, meta JSONB, created_at)
- frames (id PK, camera_id FK, s3_key, captured_at, width, height, created_at, processed boolean)
- inferences (id PK, frame_id FK, model_version, results JSONB, latency_ms, created_at)
- overlays (id PK, frame_id FK, s3_key_overlay, thumbnail_key, created_at)
- annotations (id PK, frame_id FK NULLABLE, camera_id, user_id, bbox JSONB {x,y,w,h}, label, comment, created_at, reviewed boolean)
- users (id PK, email, name, role, hashed_password, created_at)
- audit_logs (id, entity_type, entity_id, action, actor_id, payload JSONB, ts)

Indexing: add indexes for frames(camera_id, captured_at), inferences(frame_id), annotations(camera_id, created_at), and JSONB GIN indexes for query-heavy fields.

## Model serving options (cloud vs edge)
1) Cloud-hosted inference (recommended for MVP)
   - Host models in k8s cluster with GPU node pool (Nvidia A10/A100 depending on budget).
   - Containerize model with gRPC/HTTP inference interface (TorchServe / Triton / FastAPI wrapper depending on framework).
   - Pros: simpler deployment, central management, easier scaling, GPU share for burst workloads, simpler monitoring and model updates.
   - Cons: network latency for edge cameras if high bandwidth; cost of GPU instances.

2) Managed model hosting services
   - AWS SageMaker / GCP Vertex AI / Azure ML endpoints.
   - Pros: managed infra, autoscaling, easier A/B deployments.
   - Cons: higher cost; less control over GPU utilization; integration overhead for pre-signed S3 + queue flow.

3) Edge deployment (future/optional)
   - Deploy optimized models (ONNX/TensorRT) to edge devices or small edge servers per site.
   - Pros: lowest latency, lower egress cost.
   - Cons: operational complexity, OTA updates, device heterogeneity.

Decision: Start with cloud-hosted GPU-backed inference in k8s for MVP. Design the inference interface (gRPC + REST) so swapping in edge-serving is straightforward.

## Inference pipeline (detailed)
- Camera uploads frame to S3 via presigned URL.
- Backend receives ingest/frame notification → write frames record and enqueue Celery task.
- Celery worker (or k8s queue consumer) posts job to inference queue (RabbitMQ/Kafka). Use durable queue with visibility timeouts.
- Inference service consumes job, downloads S3 object (or pulls through shared FS), runs model, writes inference JSON to inferences table and stores overlay PNG to S3.
- Post-processing: create thumbnails, compute metrics, optionally run additional heuristics (confidence threshold, NMS)
- Notify frontend via websocket event + persist results.

Optimization notes:
- Batch inference where model supports batching to improve GPU throughput.
- Keep warm pools of pods to reduce cold-start GPU overhead.
- Use model warmup and JIT/optimized runtimes (TensorRT, ONNX Runtime) to reduce latency.

## Scaling plan
- Kubernetes cluster (EKS/GKE/AKS) as primary control plane.
- Node pools:
  - small CPU nodes for API, Celery workers, background jobs
  - GPU node pool (Nvidia) for inference pods (spot/preemptible nodes for cost savings where acceptable)
- Horizontal Pod Autoscaler based on CPU/queue length/custom metric (inference queue depth)
- Cluster Autoscaler to add GPU nodes when needed; use buffer capacity to handle short bursts.
- Throughput sizing example (assumptions):
  - Model average throughput per GPU: 20–100 inferences/sec depending on model. For 50/sec sustained, 1 GPU may suffice; plan 2 GPUs for redundancy and bursts.
- Use request/limits and pod disruption budgets.

## Observability & monitoring
- Tracing: OpenTelemetry instrumentation in API + inference service. Export to OTLP collector -> backend storage (Tempo / Jaeger).
- Metrics: Prometheus scraping (API, inference exporter, Celery metrics, queue length). Create Grafana dashboards for:
  - Inference latency distribution (p50/p95/p99)
  - GPU utilization per node
  - Queue depth & throughput
  - API response latency & error rates
- Logs: Structured JSON logs shipped to ELK or a managed service (Datadog/Cloudwatch).
- Alerts: SLO-based alerts: p95 latency > 200ms, error rate > 0.1%, queue depth > threshold.

## Security
- JWT + RBAC. Validate inputs strictly and sanitize JSONB fields.
- Signed presigned URLs for S3 with short TTL.
- Network segmentation: inference pods in private subnets; API gateways/ingest endpoints in public with WAF.
- Use IAM roles for service accounts (IRSA in EKS) for least-privilege access to S3/RDS.
- Secrets: store in KMS/Secrets Manager.

## Data retention & privacy
- Raw frames retention policy (default 7–30 days configurable). Move older frames to cheaper storage class (Glacier)
- Annotations & audit logs retained per compliance (configurable)

## Infra cost estimate (monthly, rough)
Assumptions: AWS, 50 concurrent streams → 50 fps total load ~50/sec; moderate dashboard usage.
- EKS control plane & worker nodes (3 x t3.medium CPU nodes) ~ $200
- RDS (db.t3.medium, 100GB gp3) ~ $200–$300
- S3 storage (1 TB hot + 5 TB cold) ~ $25–$100
- Redis (ElastiCache t3.small) ~ $50
- GPU nodes (on-demand p3/ g4/ a10):
  - 1 x g4dn.xlarge (NVIDIA T4) ~ $0.75/hr → ~$540/mo
  - For redundancy/buffer 2 nodes (or mix spot) ~ $1,000/mo
- Load balancer & NAT egress ~ $50–$150
- Managed logging / monitoring (CloudWatch/Datadog) ~ $100–$300
Estimated total (MVP): $1.5k — $3k / month (using mix of on-demand + spot GPUs). If using managed endpoints (SageMaker), expect +30–50% cost.

## Risks & mitigations
- Cost of GPUs: Use spot instances + capacity buffer; use model optimizations to reduce GPU need.
- Latency for remote cameras: consider edge option for high-latency sites.
- Operational complexity: start with a single managed cluster and minimal node types; automate CI/CD for model images.

## Next steps (implementation milestones)
1. API & DB schema -> implement endpoints and migrations (I will produce DB migrations & API routes).
2. Build inference container + simple Triton/TorchServe wrapper and test on 1 GPU node.
3. Observability instrumentation (OpenTelemetry) added from day one.
4. Performance testing with simulated camera load (50–200 fps) and adjust autoscaling.

## Open decision points (need Product input / Security)
- Retention policy defaults (7 vs 30 days) — product decision.
- Level of managed services vs self-managed (SageMaker vs k8s) — cost vs operational tradeoff.


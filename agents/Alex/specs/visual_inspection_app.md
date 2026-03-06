# Feature: Visual Inspection App (Factory) - MVP
**Goal:** Build an intuitive visual inspection application to detect defects on production lines in real-time and store inspection events for analysis and traceability.

**North Star Impact:** Reduce undetected defects and inspection cycle time; increase first-pass yield and operator trust in automation.

**Users:**
- Production line operators: run inspections, view alerts, acknowledge events.
- Quality engineers: review defect logs, tune models, generate reports.
- Plant managers: monitor KPIs (defect rate, MTTR).

**RICE Score:** Reach=500 production lines/quarter × Impact=2 (performance) × Confidence=70% / Effort=8w = 87.5

**Kano Category:** Performance (must improve inspection throughput and accuracy)

**Acceptance Criteria:**
- [ ] Operator can register a production line and attach one or more camera sources.
- [ ] Operator can start/stop live inspection per line and receive real-time defect alerts in the UI.
- [ ] Backend ingests frames (edge or cloud), runs inference, and returns per-frame results within 1s (edge) / aggregated results within 3s (cloud) for MVP.
- [ ] System persists inspection events and associated snapshot images to storage with metadata (timestamp, line_id, camera_id, defect_type, confidence).
- [ ] Dashboard allows filtering by time, line, and defect type and exports CSV for a selected time window.
- [ ] Accuracy baseline for deployed model: precision >= 90% and recall >= 85% on validation dataset (MVP target; model training pipeline is out of scope).
- [ ] System tolerates network disruption: camera-edge buffers up to 5 minutes of frames and uploads when connectivity resumes.
- [ ] Concurrency: platform supports 100 concurrent camera streams for MVP; performance degradation documented in runbook.
- [ ] Security: role-based access (operator, engineer, admin). Sensitive data storage follows encryption-at-rest.

**Out of Scope:**
- Training new ML models end-to-end (only inference and model deployment supported in MVP)
- Mobile native app (web-first)
- Deep MES / ERP bidirectional sync (export API only)

**Success Metrics:**
- Defect detection adoption: >60% of lines enrolled within 3 months
- Detection precision >=90% and recall >=85% in production
- Mean time to acknowledge alert < 2 minutes
- System availability >= 99.5% for critical inspection endpoints

**Architecture notes (high level):**
- Edge inference recommended per line for latency: run model in container on edge gateway; fallback to cloud inference if edge unavailable.
- Backend: REST API + event queue for ingestion, object storage for snapshots, relational DB for metadata, simple rules engine for alerting.
- Telemetry: per-stream metrics, model confidence histogram, error rates.

**GitHub Issue:** TBD

**Files created:** output/specs/visual_inspection_app.md

**Next steps:** Create GitHub issue, estimate effort, and hand off to backend to propose API + DB schema and deployment plan.

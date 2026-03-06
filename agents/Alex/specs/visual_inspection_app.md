# Feature: Visual Inspection App (Factory)
**Goal:** Build an intuitive, scalable visual inspection application to detect manufacturing defects in real-time and surface them to operators for immediate action.

**North Star Impact:** Reduce defect escape rate and rework costs; improve production throughput and QA efficiency.

**Users:**
- Primary: Line Operators — use camera UI to inspect parts and confirm/reject defects.
- Secondary: Quality Engineers — analyze defect trends, tune models, and review edge cases.
- Stakeholders: Plant Manager / Ops — monitor KPIs and compliance reports.

**RICE Score:** Reach=500 (operator sessions per quarter) × Impact=2 (moderate) × Confidence=70% / Effort=8w = 87.5

**Kano Category:** Performance (high ROI when accurate and fast)

**Scope & Key Capabilities:**
- Live camera ingestion (RT or near-RT) with overlay of detections
- Snapshot capture + manual labeling workflow for false positives/negatives
- Inference: run ML model (edge or cloud) and return per-item classification + confidence
- Dashboard: defect counts, trend charts, sample images, operator actions
- Integration: export defects to factory MES via REST webhook
- Auth & audit logs: user actions, image retention policy

**Acceptance Criteria:**
- [ ] Operator can view a live camera feed and receive bounding-box / label overlays for detected defects.
- [ ] System returns inference result for each captured item in <200ms (p99) for edge deployment; <500ms for cloud inference.
- [ ] Base ML model achieves >=90% precision and >=85% recall on validation set (initial target).
- [ ] Operator can mark detection as true/false positive; labeled images are stored for retraining.
- [ ] System supports 10 concurrent camera streams per backend instance (scalability target) and horizontal scale.
- [ ] Audit trail records user decisions and model version for each inspected item.
- [ ] Secure access: SSO or company LDAP integration (or token-based auth) for operator access.

**Out of Scope:**
- Automated continuous model retraining & deployment pipeline (MVP will collect labeled data for offline retraining).
- Deep MES integration beyond a webhook export.

**Success Metrics (post-launch):**
- Precision >=90% and Recall >=85% on production validation within 6 weeks.
- Defect escape rate reduced by 40% in 3 months.
- Operator adoption: >60% of shifts using the app daily.
- Mean time to acknowledge a defect <5 minutes.

**Risks & Mitigations:**
- Model drift → mitigate by collecting operator-labeled samples and scheduled model reviews.
- Bandwidth/latency constraints → support edge inference and adaptive frame sampling.
- Operator trust → provide easy override + audit logs + confidence scores.

**GitHub Issue:** TBD

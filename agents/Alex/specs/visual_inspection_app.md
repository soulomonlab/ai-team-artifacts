# Feature: Visual Inspection App
**Goal:** Provide factory operators an intuitive app to capture, annotate, and manage visual inspection (defect detection) workflows that scales to multiple factories and maintains high code quality.

**North Star Impact:** Reduce manual inspection time by 50% and increase defect detection rate by 30% within 6 months of deployment.

**Users:**
- Primary: Line operators doing visual inspection on assembly lines (capture images, mark defects, submit reports).
- Secondary: QA engineers and supervisors (review reports, analytics, audit trail).
- Admin: Dev/Ops for deployment, model ops for ML improvements.

**RICE Score:** Reach=[200 factories × 50 lines ≈ 10,000 operators/quarter] × Impact=[1.5 (meaningful improvement)] × Confidence=[70%] / Effort=[8w] = (10,000 × 1.5 × 0.7) / 8 ≈ 1,312.5

**Kano Category:** Performance / Must-have for large customers

**Core Capabilities (MVP):**
- Real-time image capture from a web/mobile client (camera integration)
- Guided inspection workflow: step list per product, pass/fail + defect type tagging
- Annotation tools: bounding boxes, freehand marks, severity tag
- Report submission with metadata (line, SKU, operator, timestamp)
- Secure storage of images + metadata with scalable object storage
- Admin dashboard: recent inspections, defect counts, filter/search
- Exportable audit logs and CSV reports

**Acceptance Criteria:**
- [ ] Operator can capture or upload an image and attach it to an inspection record.
- [ ] Operator can annotate image (bounding box + label) and submit inspection.
- [ ] System stores image in scalable object storage and returns a stable URL within 2s.
- [ ] Submitted inspection appears in QA dashboard within 5s; searchable by SKU, line, operator.
- [ ] API responds <200ms for metadata endpoints under 100 RPS; image upload throughput scalable (S3 presigned URLs).
- [ ] Audit log records user, action, timestamp for every inspection event.
- [ ] Role-based access control: operators vs QA vs admin.
- [ ] End-to-end tests for happy paths + edge cases present in tests/ directory.

**Out of Scope (MVP):**
- Automated ML-based defect classification (optional for v1; will be introduced as an integration in v2).
- Offline-first mobile operation (v1 requires network connectivity).

**Non-functional Requirements / Constraints:**
- Scalability: object storage (S3-compatible), stateless API instances behind load balancer.
- Security: images encrypted at rest, RBAC, audit logs retained 1 year.
- Code quality: 80% unit test coverage for backend, linting, CI gating.

**Success Metrics:**
- Adoption: >60% of lines using the app within 3 months.
- Accuracy: manual QC shows 30% higher defect detection vs baseline.
- Performance: metadata API p95 < 200ms under target load.
- Reliability: 99.9% uptime for API layer.

**Dependencies:**
- Camera hardware + browser/mobile support (product to validate supported devices)
- Object storage (S3)
- Auth service (SSO) or initial internal user DB

**Next Steps / Deliverables:**
- Backend architecture & API spec (owner: Marcus)
- Frontend wireframes and interaction spec (owner: Maya)
- QA test plan and acceptance tests (owner: Dana)

**GitHub Issue:** (created by PO) #

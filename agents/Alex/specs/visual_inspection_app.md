# Feature: Visual Inspection App for Manufacturing
**Goal:** Build an intuitive web application that enables floor operators and quality engineers to perform automated visual inspection of manufactured parts, detect defects in real-time, and track inspection metrics.

**North Star Impact:** Reduce manual inspection time by 60% and decrease escaped defects by 50% within 6 months of launch.

**Users:**
- Operator (floor worker): quickly inspect parts during production, receive pass/fail guidance, annotate defects.
- Quality Engineer: review defect trends, tune detection thresholds, export reports.
- Plant Manager: monitor KPIs across lines and shifts.

**RICE Score:** Reach=120 factories per quarter × Impact=2 (meaningful) × Confidence=70% / Effort=6w = 28

**Kano Category:** Performance (core feature; more accurate & faster = better)

**MVP Scope (must-have):**
- Web app dashboard for live camera feed and historical inspections
- Automated defect detection using pre-trained vision model (edge or cloud inference)
- Manual annotation tool (bounding boxes + label) to correct predictions
- Per-line/per-shift defect metrics and CSV export
- User roles: operator, quality_engineer, plant_manager

**Acceptance Criteria:**
- [ ] Operator can open the app and connect to a camera (RTSP or USB) and see live video with <1s lag under on-prem network conditions.
- [ ] System runs inference on each frame and overlays defect bounding boxes with confidence scores.
- [ ] Operator can accept/reject detection and add annotation; annotations persist and are visible in the dashboard.
- [ ] Quality Engineer can view defect trends by line, shift, and part number for last 30/90/365 days.
- [ ] Export: Quality Engineer can download inspection data as CSV for a selected time range.
- [ ] Authentication & RBAC: users can sign in and have role-based UI (no admin endpoints exposed to operators).
- [ ] System handles 10 concurrent camera streams per server instance (performance target) with average inference latency <250ms/frame for final model.
- [ ] Error handling: when a camera disconnects, operator sees clear recovery flow and reconnection attempt every 5s.

**Out of Scope (MVP):**
- Full MLOps pipeline for continuous model training (will be planned as next phase)
- Mobile-native app (web-first)
- Complex workflow integrations (ERP/MES) beyond CSV export

**Success Metrics:**
- Time saved per inspection session (avg) — target: -60% vs manual baseline
- Defect escape rate reduction — target: -50% after 6 months
- Operator adoption rate: % of inspections performed via app — target: >60% after 3 months
- False positive rate and false negative rate for defect detection — targets TBD after model evaluation

**Technical Constraints / Decisions so far:**
- Support RTSP and USB camera ingestion for on-prem flexibility.
- Start with cloud-hosted inference but design for edge inference as a deployable option (reversible decision).
- Use roles for RBAC; integrate with SSO later (out-of-scope for MVP).

**Acceptance Tests (QA):**
- Live camera connectivity test (RTSP emulated stream)
- Annotation persistence test (create, edit, delete)
- Load test with 10 concurrent streams (simulate network conditions)
- Security test: verify RBAC prevents operator access to admin endpoints

**GitHub Issue:** created (see linked issue in task)

**Next Steps:**
- Technical owner to propose architecture (API design, model hosting strategy, scaling plan)
- Designer to provide wireframes for operator live-inspection flow + dashboard
- Frontend to implement camera-connect + annotation components
- QA to prepare acceptance test cases and load test plan


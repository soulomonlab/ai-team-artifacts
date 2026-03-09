# Audit Dashboard Prototype Spec

Goal
- Minimal dashboard for compliance auditors to query model inference logs, filter by model/version/time/user hash, and export signed manifests for investigations.

User personas
- Compliance auditor: read-only access to query logs and export snapshots.
- Security analyst: deeper access with ability to flag records and request raw payloads under approval.

Functional requirements
1. Query interface
   - Filter by: model_id, model_version, time range, request_id, hashed_user_id, prediction range, confidence threshold.
   - Pagination and sorting.
2. Record view
   - Show summary fields: timestamp, model, version, input_summary, output_summary, pii_flags, hmac_signature, access_history.
   - Link to raw input object (subject to approvals). 3-click request flow for access.
3. Exports
   - Export search results to signed Parquet/CSV with manifest signed by HMAC key.
4. Audit actions
   - Flag record (reason), annotate, and trigger incident ticket.
5. Access control
   - RBAC: role mapping (auditor, security_analyst, admin). SSO/OAuth2 integration.

Non-functional
- Data retention policies enforced in the backend.
- UI shows data redaction indicators when PII was masked.
- Tamper-evident markers for record sets.

MVP UI flow
- Landing: quick search bar + recent alerts.
- Results table: columns timestamp, model_id, version, prediction, confidence, pii_flag, actions.
- Record modal: detailed view + export/flag buttons.

Tech stack suggestions
- Frontend: React + TypeScript, MUI for components.
- Backend: FastAPI + Postgres/ClickHouse for summary queries.
- Auth: OAuth2 with OIDC SSO; permissions via RBAC table.
- Signing: HMAC via Vault secrets, export signed before download.

Acceptance criteria
- Search by model_id and time range returns matching synthetic events in test env.
- Export produces a signed manifest and file.
- RBAC prevents auditor from accessing raw inputs without approval.

Open questions / next actions
- Which DB for hot queries (Postgres with optimized indexes vs ClickHouse)? Recommend ClickHouse if high QPS and analytical queries.
- Approvals workflow integration with ticketing (Jira) for raw access.


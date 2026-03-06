Threat Model & Implementation Plan (MVP)

Summary
- Goal: Secure IaC skeleton for production secrets, enforce TLS, add CI scanning, and baseline K8s security controls.
- Priority items: Vault (or cloud secret manager) for secrets, mandatory TLS/HSTS, DB TLS enforcement, CI SAST + image scanning (Bandit + Trivy), and K8s PodSecurity + resource limits.

Key Decisions
1. Secrets: Primary = HashiCorp Vault (self-managed or managed: HCP). Fallback = cloud provider secret manager (AWS Secrets Manager / GCP Secret Manager) if HCP not approved.
   - Rationale: centralized secrets lifecycle, dynamic credentials, audit logs.
2. TLS: TLS mandatory for all ingress and service-to-service comms. Enforce HSTS at edge (nginx/ALB) and require DB TLS connections.
3. CI Scanning: Bandit (Python SAST) + Trivy (container image & filesystem). CI will NOT contain plaintext secrets; usage via GitHub Secrets + Vault pull on deploy.
4. K8s Security Baseline: Use PodSecurity admission with 'restricted' for production namespaces, set CPU/memory resource requests & limits, enable read-only root filesystem where possible.

Implementation Plan (MVP)
- IaC / Secrets
  - Add Vault module to IaC skeleton (Terraform): vault cluster or connector to cloud secret manager.
  - Provide fallback variables & module to use AWS/GCP secret manager if Vault flag is false.
  - Auth model: Kubernetes auth (k8s service account -> Vault) or AppRole for non-k8s runners.
  - Store minimal bootstrap secrets in CI as short-lived tokens (VAULT_ROLE_ID/VAULT_SECRET_ID) — never plain DB passwords.

- TLS / HSTS / DB TLS
  - Ingress: enforce TLS redirect + HSTS header in ingress controller (nginx-ingress or ALB) config.
  - Internal: mTLS is recommended for service-to-service (future), but initial requirement: TLS for DB and external endpoints.
  - DB connections: require sslmode=require and verify-server-cert where supported.

- CI Pipeline
  - Add SAST job (Bandit) on PRs: fail PR if medium/high issues found.
  - Add Trivy image scan after docker build in CI: fail on HIGH/CRITICAL vulns.
  - Ensure CI does NOT echo secrets; use GitHub Actions masking and environment secrets.

- K8s Baseline
  - PodSecurity for prod namespace = restricted.
  - Resource quotas & limit ranges per namespace.
  - Liveness/readiness health checks required on all Deployments.
  - Image pull policy and immutable tags; enable image scanning on registry.

Acceptance Criteria
- IaC contains Vault module + fallback docs.
- CI contains Bandit and Trivy scanning jobs; failing thresholds defined.
- K8s baseline doc and example manifest with PodSecurity labels and resource limits.

Action Items (MVP)
1. Create IaC Vault module + example (Noah/Marcus): skeleton + docs. (Next: Marcus implement in repo)
2. Add TLS/HSTS defaults in ingress module (Marcus/Taylor alignment required).
3. Add CI jobs (Noah) — Bandit + Trivy; open PR for review.
4. Add K8s PodSecurity & resource examples (Noah) — handoff to Marcus to adopt.

Notes / Dependencies
- Coordinate with Taylor (#ai-tech-lead) for final infra topology (managed Vault vs cloud secrets) before prod rollout.
- Security owner: Isabella to sign-off on thresholds and Vault choices.

References
- Trivy docs: https://aquasecurity.github.io/trivy/
- HashiCorp Vault: https://www.vaultproject.io/

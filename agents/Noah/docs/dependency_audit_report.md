Dependency & IaC Audit — Initial Findings and Plan

Scope
- Inventory: application dependencies (python/node), docker base images, terraform providers, helm charts, k8s manifests.
- Tools: Snyk (app & container), Dependabot alerts, ORT/tfsec/checkov (IaC), tflint (provider checks).
- Timeline: Inventory within 3 business days; patches targeted within 5 business days after inventory complete.

Findings (placeholder — run scans to populate):
- Python packages: [to be filled]
- Node packages: [to be filled]
- Docker base images: [to be filled]
- Terraform providers: [to be filled]
- Helm charts: [to be filled]

Strategy and Rules
1) CI gating policy
   - Fail CI on any NEW critical or high CVE introduced by a PR.
   - Existing baseline: current moderate CVEs are allowed but must be tracked in a project board and addressed in scheduled sprints.
   - Dependabot auto PRs for patch-level upgrades; security team to review major upgrades.

2) IaC plugin/provider vulnerabilities
   - Run provider plugin checks (tflint + provider-specific advisories).
   - If vulnerabilities found, create a 'devops' issue with remediation plan and ETA.

3) Staging deployment & smoke test
   - Any patch that modifies runtime or infra modules must deploy to staging with smoke tests (health endpoint, simple API flow).
   - Use blue/green or rolling update to reduce blast radius.

Next actions
- Add CI job for dependency and IaC scans (created: output/config/ci_dependency_checks.yml).
- Run Snyk, ORT, tfsec, checkov, tflint locally/CI and populate findings in this report.
- Schedule coordination meeting with Marcus (#ai-backend) to plan risky upgrades and identify required app changes for patched dependencies.

Contact
- DevOps: Noah
- Backend owner: Marcus
- Dependency owner: Dependency

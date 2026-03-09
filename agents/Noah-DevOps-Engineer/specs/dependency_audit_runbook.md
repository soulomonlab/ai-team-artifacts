Dependency Audit Runbook - DevOps Actions

Purpose
- Standardize how DevOps will run dependency and IaC audits, triage findings, and coordinate patches.

Pre-requisites
- Ensure SNYK_TOKEN and GITHUB_TOKEN are set in repo secrets.
- Local tools: docker, jq, terraform, trivy, ORT (ossreviewtoolkit) or its container image.

Step 1: Inventory providers and modules
- Run script (example):
  - find . -name "*.tf" -exec dirname {} \; | sort -u | xargs -I{} bash -c "(cd {} && terraform providers > providers.txt) || true"
- Aggregate providers into output/data/iac_providers_inventory.csv with columns: repo_path, provider, version, file_path

Step 2: Static scans
- Run ORT container scan (creates ort-result.yml)
- Run trivy filesystem scan for k8s manifests and helm charts: trivy fs --format json -o trivy-iac.json .
- Run Snyk for dependencies and images as in CI job. Save JSON outputs.

Step 3: Map to CVEs and prioritize
- For each provider version, query NVD or vendor advisories. Tools: vulners API, GitHub advisory API.
- Assign priority: P0 (critical), P1 (high), P2 (moderate), P3 (low).

Step 4: Patch & test
- For P0/P1 findings: create infra branch, bump provider version, run `terraform init -upgrade`, run terraform plan in staging workspace.
- Deploy to staging (k8s or cloud infra), run smoke tests (health check endpoints, DB connectivity, etc.).
- If tests pass, open PR for merge and schedule production rollout with Marcus.

Step 5: Record baseline
- For existing moderate findings, record them in 'dependency-baseline.json' with justification and suppressions (if any).
- Use Snyk monitoring policies or .snyk ignore rules to avoid blocking PRs for baseline items.

Escalation
- If a provider bump results in infra breakage, revert and open a post-mortem ticket. Notify Marcus and Dependency team immediately.

Templates & Scripts
- Provide helper scripts in output/scripts/ (create as needed):
  - inventory_providers.sh
  - run_ort.sh
  - run_trivy_iac.sh


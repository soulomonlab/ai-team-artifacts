Dependency CI & IaC Audit — README

Files added:
- output/config/ci_dependency_checks.yml — GitHub Actions CI workflow to run Snyk, tfsec, checkov, tflint and placeholder for ORT.
- output/docs/dependency_audit_report.md — Initial audit plan and rules for gating.
- output/code/run_iac_scans.sh — Script to run IaC scanners locally or in CI and collect outputs.

Secrets required (add to repo Settings → Secrets):
- SNYK_TOKEN
- GITHUB_TOKEN

How to run locally
1. Install tools: pip install tfsec checkov; npm i -g snyk; install tflint; install ORT if needed.
2. Run: ./output/code/run_iac_scans.sh . ./output/reports/iac

Next steps
- Run the CI workflow on a branch to collect findings.
- Coordinate with Marcus (#ai-backend) for remediation of high/critical issues.
- After findings, create issues with 'devops' label containing remediation ETA.
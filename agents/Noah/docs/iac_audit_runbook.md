IaC Dependency Audit & Runbook

Purpose:
- Provide step-by-step instructions to run ORT and other IaC scans, collect plugin/provider vulnerability inventory, and triage results.

Scope:
- Terraform modules, Kubernetes manifests, Helm charts, provider plugins.

Prerequisites:
- ORT installed (https://oss-review-toolkit.org)
- Docker (for ORT analyzer)
- Access to repo and state files (if scanning Terraform state)

Steps:
1. Install ORT
   - curl -sL https://raw.githubusercontent.com/oss-review-toolkit/ort/master/installer/install.sh | bash
2. Prepare analyzer configuration
   - Create ort-config.yml with repository layout and analyzers enabled
3. Run ORT analyzer on IaC directories
   - ort analyze --input-path ./iac --output-file ort-output.yml
4. Run ORT reporter to create human-readable report
   - ort reporter --input ort-output.yml --output-dir ort-report
5. Extract provider/plugin vulnerabilities
   - Inspect ort-report for 'analyzer - terraform' sections; list plugin versions
6. Cross-reference plugin versions with CVE databases and provider advisories
7. Produce inventory.csv with columns: component,type,version,CVE,severity,remediation

Acceptable Baseline Policy:
- Existing moderate CVEs allowed (documented in agents/Dependency/docs/dependency_audit_plan.md)
- New critical/high CVEs introduced by a PR must block the PR

Post-scan actions:
- Create issues for each high/critical finding, tag @Marcus and @Dependency
- For provider plugin issues, check whether upgrading Terraform or provider is needed; test in staging
- Schedule patch deployment within 5 business days for critical/high findings

Notes:
- ORT config is repo-specific. For the initial run, run locally and attach ort-report to the issue.
- Use Snyk for runtime and dependency scanning for application code.

CI Dependency Gate Policy

Goal:
- Block PRs that introduce new critical or high CVEs. Allow baseline moderate issues while documenting them.

Checks added to CI (see output/config/ci_dependency_checks.yml):
- Snyk: scans application dependencies and fails if new high/critical vulnerabilities are introduced.
- Dependabot alerts check: surface GH advisory alerts.
- ORT for IaC scanning: detects provider or module issues.

Enforcement logic:
1. For each PR, run Snyk test and save JSON output (snyk test --json).
2. Compare the JSON against the last main branch baseline report stored in /ci/baseline/snyk.json.
3. If PR introduces any CVE with severity >= HIGH that is not in baseline, fail CI and require remediation.
4. For moderate CVEs, allow but annotate PR with details and require an owner to triage within 7 business days.

Baselining process:
- Initial baseline run will be performed across main branch; results stored in /ci/baseline/snyk.json and /ci/baseline/ort-report.
- Update baseline only after an approved ticket and risk assessment (assign to Dependency team).

Required GitHub Secrets:
- SNYK_TOKEN

Integration notes:
- CI action will output files: snyk-output.json, ort-output.yml, dependabot-summary.json
- UI annotations will be used for clear visibility in PRs

Escalation:
- New critical findings -> immediate P0 escalation to #ai-security and @Isabella, block merge
- High findings -> P1, notify Marcus and Dependency


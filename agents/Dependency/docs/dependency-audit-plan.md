Dependency audit plan

Goal
Run a full dependency audit to identify outdated and vulnerable packages across the repo and produce a prioritized remediation list.

Scope
- All code subdirs (backend, frontend, mobile, infra config)

Tasks
1. Run automated scanners (Dependabot/Snyk/GitHub-Advanced-Security/OWASP) and language-native checks (npm audit, pip-audit, go list -m -u, etc.).
2. Produce a single report: package, current version, latest safe version, CVE(s), severity, exploitability, suggested PR target version, estimated risk/time to upgrade.
3. Flag any transitive dependencies that require major upgrades or code changes.
4. Include quick mitigation notes (temporary overrides, runtime workarounds, or config changes) if immediate patching is unsafe.

Acceptance criteria
- Report uploaded to output/reports/dependency-audit.md in the repo (or attached to this issue).
- Triage table with prioritization: Critical/High -> Medium -> Low.
- Assign follow-up upgrade issues for Critical/High items.

Notes / Risk
- Some upgrades may be breaking (major version). Mark those as requiring feature-flagged rollout or staging validation.

Hand-offs
- #ai-backend (Marcus): run local scans and review results.
- #ai-security (Isabella): validate CVE severity and exploitability.
- #ai-devops (Noah): ensure scanners have access to private modules/artifacts.

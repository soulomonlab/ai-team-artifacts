Dependency audit - initial run

Summary
- Run Dependabot + Snyk/OSV to enumerate outdated/vulnerable dependencies across stacks.

Findings (placeholder - run scans to populate)
- TODO: populate with package, current version, CVE ids, severity, recommended upgrades.

Recommendations
- Prioritize CRITICAL/HIGH vulnerabilities for immediate PRs.
- Coordinate major-version upgrades with #ai-frontend and #ai-devops.

Next steps
1. Trigger scans (Dependabot & Snyk/OSV).
2. Create remediation PRs for critical/high.
3. Add detailed report to this file.

Risk notes
- Major bumps may require integration testing and DB migrations.


Dependency audit — initial plan and quick recommendations

Summary
- Purpose: baseline dependency hygiene and track upgrades before staging provisioning and OpenAPI work.
- Next action: run automated SCA across repo (npm / pip / go) and produce per-ecosystem findings + PRs. Target: report by EOD tomorrow.

Immediate recommendations (safe, minimal-risk)
- API server / Python backends:
  - Pin DB drivers to latest stable minor releases compatible with our Postgres: prefer psycopg (psycopg>=3.x) or psycopg2-binary >= latest 2.9.x patch. Test local/staging compatibility.
  - redis-py: upgrade to latest 4.x stable.
- Node services:
  - Bump patch/minor only (no major bumps) for express, lodash, axios to latest stable patch/minor to avoid breaking changes. Run npm/audit and npm update --depth 0, then test.
- General: regenerate lockfiles (package-lock.json / Pipfile.lock / poetry.lock / go.sum) after upgrades and run CI tests.

Risk notes
- Major upgrades can break runtime compatibility; prefer patch/minor upgrades. For any major-version bump open a separate PR with migration notes and tests.
- DB driver upgrades should be validated against Postgres staging (we have approved Postgres+Redis). Coordinate with #ai-backend and #ai-devops.

Automated checks to run
- npm audit / npm audit fix --force (only after review)
- pip-audit and safety check for Python
- go list -m -u all and vuln checks for Go

Deliverables
- Per-ecosystem vulnerability report
- PRs per upgrade (small, focused)
- Tracking issues for critical upgrades + risk notes

File created by Dependency. Follow-up: I will open tracking issues and schedule fixes.
Dependency Audit Plan for MVP (Owner: Dependency Agent)

Goals:
- Inventory all dependencies across repo
- Find critical/high vulnerabilities and patch them before MVP
- Add CI gates to prevent regressions

Scope:
- Backend (services/)
- Frontend (web/)
- Mobile (mobile/)
- IaC (infra/)
- ML (ml/)

Tools to use:
- GitHub Dependabot
- Snyk
- OSS Review Toolkit (ORT)
- npm audit, pip-audit, mvn dependency:tree

Deliverables:
- output/reports/dependency_inventory.csv
- output/reports/vuln_summary.md
- PRs/branches for patches (refs in report)
- CI config additions file: output/config/ci_dependency_checks.yml

Timeline:
- Audit + inventory: 3 business days
- Critical/high PRs: within 5 business days
- CI gates + baseline: within 7 business days

Coordination:
- Work with Marcus (backend) for any API/integration tests impacted
- Work with Noah (DevOps) for infra config changes


# Target User Persona & Launch Constraints

## Target personas

1) Primary: Product Managers (PMs) at SMB / early-stage startups
- Age: 25–40, tech-savvy, frequently coordinates cross-functional teams
- Goals: Quick setup, track feature progress, invite teammates, minimize onboarding friction
- Devices: Mobile-first use for quick checks; desktop for deeper work
- Pain points: Complex signups, slow onboarding, unclear success metrics

2) Secondary: Team leads / Operations managers
- Needs: Role-based access, audit trails, SSO support

## Recommended launch deadline (MVP)
- Target: End of Sprint 2 — 2026-03-31 (4-week delivery cadence starting now)
- Reason: Gives design + frontend + backend one sprint each for core flows and buffer for QA

## Hard constraints & non-functional reqs
- Mobile-first by default (responsive desktop)
- Accessibility: WCAG AA baseline
- Privacy/Compliance: GDPR by default; HIPAA only if customer request (flag and scope separately)
- Data residency: default global; EU-only tenant option required (store EU tenant data in EU region)
- Auth: support email+password + SSO (OIDC/SAML) at launch
- Rate limiting: per-tenant and per-user throttles
- Scalability: design for multi-tenant DB and horizontal scaling

## Key UX decisions (made now)
- Onboarding: progressive, 3-step flow (Account → Team → Quick Tour) to reduce drop-off
- First-run experience: pre-populated sample project + inline tooltips
- Minimal fields at signup (name, email, password) with optional company name
- Invite flow: email invite + role selection modal (Admin / Member)
- Empty states: actionable CTAs and 1-click sample data import
- Error handling: inline form errors + global toast for system errors

## Component & design system guidelines
- Grid: 8px spacing system
- Typography: Inter (weight set: 400/500/600/700)
- Colors: Primary (brand) + neutral palette; accessible contrast >4.5:1 for body text
- Buttons: Clear primary action, ghost secondary, icon-only for tight spaces

## User flows (high level)
1) Sign up (email/SSO) → Create/Join team → Create first project → Guided tour
2) Invite user → Assign role → User accepts via email → lands on project
3) Sign-in error flow → Inline help + support CTA

## Wireframe (ASCII)
Onboarding screen (mobile):

[Header: Brand]

[Step indicator: ● ○ ○]

[Card: Create your team]
- Team name (input)
- Continue (primary button)

[Footer: Log in | Terms]


## Notes / Risks
- If HIPAA becomes required, we need separate scoping for encryption, BAAs, and logging — this will delay launch.
- EU data residency requires infrastructure decisions (region-specific DB) — backend estimate required.

---
Design file created for handoff to backend for estimates.

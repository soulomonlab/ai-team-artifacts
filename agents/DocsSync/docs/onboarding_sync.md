Onboarding — DocsSync summary

Source: agents/Maya/design/onboarding_sketches.md (mid-fi spec + wireframes)

Key decisions (locked for kickoff)
- Card-first task layout for scanability
- Onboarding = 3 screens max (Welcome → Account → Preferences)
- Starter brand color: #2563EB (design to confirm final tokens)

Handoffs & owners
- #ai-frontend — prepare component list, feasibility concerns, and implementation estimates. Blockers: logo + final color tokens. ETA: review by 2026-03-12.
- #ai-docs — Emma to provide final onboarding CTA copy by 2026-03-09.
- #ai-design — Maya to deliver PDF/PNG mid-fi mockups by 2026-03-10.
- #ai-qa — create test plan for onboarding flows (happy path, email sign-up, social sign-in if enabled, analytics). ETA: 2026-03-13.
- #ai-devops — prepare secrets/credentials for OAuth providers if social sign-ins approved.
- #ai-security — review privacy/consent implications for social sign-in options.

Open questions & recommendations
1) Social sign-ins (Google/Apple)? Recommendation: email-first to reduce drop-off; implement social sign-ins as optional, behind a feature flag if required by stakeholders/regulators. If enabled, make Google sign-in first priority (widest reach); Apple only if mandatory for iOS app distribution.
2) Brand assets: need logo + final color palette (tokens) from #ai-design to lock visuals.

Operational impact
- Auth: adding OAuth providers requires credential provisioning, redirect URI management, and secure storage of client secrets.
- Analytics: instrument events for screen views, CTA clicks, account creation, and sign-in method chosen.
- Rollout: gate new onboarding behind a feature flag and release to a small % for monitoring.

Rollback note
- Ensure no destructive DB migration in onboarding rollout. If regressions occur, disable feature flag to revert to prior onboarding flow quickly.

Next steps (this sprint)
- #ai-frontend: component list + feasibility (due 2026-03-12).
- #ai-docs/Emma: CTA copy (due 2026-03-09).
- #ai-design/Maya: final assets (due 2026-03-10).

Links
- Design spec (mid-fi): agents/Maya/design/onboarding_sketches.md


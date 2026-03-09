CONTRIBUTING — Repository Guidelines

One-line rule:
- Frontend: Always use write_file for front-end artifacts (component mockups, design tokens, story examples). Binary assets (design files, large images) must be pushed via push_to_artifact_repo. See: output/specs/writefile_workflow.md

Frontend developer note

Purpose
- Ensure front-end artifacts are tracked in the repository and discoverable by the team. Use write_file to create text- or code-based artifacts so they appear in the output/ tree.

Where to put files
- Component code & examples: output/code/frontend/
- Component mockups & lightweight SVGs: output/design/frontend/components/
- Design tokens (JSON, CSS vars): output/design/tokens/
- Tests and QA fixtures: output/tests/frontend/
- Large/binary design files (Figma exports, .sketch, .png >1MB): push via push_to_artifact_repo (see process below)

How to create and reference artifacts
1. Create the artifact locally and use the write_file tool to write it into the appropriate output/ subdirectory. This guarantees traceability and CI visibility.
2. Reference design assets in PR descriptions and specs using their output/ path (e.g., output/design/frontend/components/Button.sketch) or an external URL if stored outside the repo.
3. For binary assets, use push_to_artifact_repo and include the returned artifact path/commit in your PR and the writefile_workflow spec link.

Handoff & task tracking
- For any tracked task that requires coordination, use handoff_to to assign the next owner so the task is recorded and a Slack notification is produced.
- Always include the output/ path(s) you created in the handoff context.

Acceptance and review
- Follow the writefile_workflow: write_file for internal artifacts; push_to_artifact_repo for binaries; handoff_to for tracked tasks. Link: output/specs/writefile_workflow.md

Contact points
- #ai-design — For design asset questions
- #ai-backend — For API / asset-serving questions
- #ai-qa — For test/edge-case expectations


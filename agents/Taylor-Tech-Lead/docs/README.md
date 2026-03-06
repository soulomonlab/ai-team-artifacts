MVP Infra & Architecture

Files created:
- docs/DECISIONS.md : Architecture decision and rationale
- code/terraform_skeleton.tf : Terraform skeleton for AWS (VPC, ECS, ECR, RDS)
- code/variables.tf : Terraform variables
- config/github_actions_ci.yml : GitHub Actions CI pipeline template

Next step: Handoff to Marcus (#ai-backend) to implement Dockerfile, FastAPI app skeleton, Alembic migrations, and to integrate OpenTelemetry. See handoff details in Slack message.
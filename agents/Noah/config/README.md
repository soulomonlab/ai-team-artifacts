Dev infra provisioning for Postgres, Redis, and Vault

What I provisioned:
- AWS VPC with private subnets and minimal SGs
- RDS Postgres dev instance + script to create ci_test DB
- ElastiCache Redis single node with transit encryption and AUTH token
- Vault on an EC2 instance (dev-only) with KV, Transit, and PKI mounts
- Vault AppRole for CI called 'ci-backend-role-dev'

Decisions:
- AWS chosen for speed and managed services (RDS/ElastiCache).
- Vault runs on single EC2 in dev (not production-ready). Recommend HCP or HA cluster in prod.
- Redis AUTH token stored in Vault; Redis TLS enabled via ElastiCache.
- CI will authenticate to Vault using AppRole (short TTL tokens). We can later add OIDC for GitHub Actions.

Next steps (for Marcus):
- Implement /health endpoint and provide app DB user creation SQL (app_user) and CI user SQL (ci_user).
- Configure backend to fetch DB and Redis creds from Vault paths: secret/data/dev/postgres/app-creds and secret/data/dev/redis/auth

Vault paths created (logical):
- secret/data/dev/postgres/app-creds  (app DB creds)
- secret/data/dev/postgres/ci-creds   (CI DB creds)
- secret/data/dev/redis/auth          (Redis AUTH token)
- transit/keys/jwt-signing-key        (Transit key for JWT signing)

How to access:
- Terraform requires VAULT_ROOT_TOKEN env or variable for initial vault provider actions.
- Do NOT commit real tokens; use GitHub Secrets for CI.

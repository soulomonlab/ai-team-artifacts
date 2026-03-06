Vault bootstrap & runbook (dev)

1) Bootstrap Vault (one-time)
- SSH into vault EC2 and export VAULT_ADDR and VAULT_TOKEN (root token produced during init)
- Run: vault operator init -key-shares=1 -key-threshold=1 > /root/vault_init.txt
- Store unseal key in a secure location (use local encrypted store)
- Run: vault operator unseal <unseal_key>
- Login: vault login <root_token>

2) Enable mounts & policies (Terraform handles if provider has token)
- KV mount: secret/ (v2)
- Transit mount: transit/
- Create transit RSA key: vault write -f transit/keys/jwt-signing-key type=rsa-2048
- Create policies: app-policy-dev, ci-policy-dev (see Terraform config)
- Create approle: role=ci-backend-role-dev with token TTL 1h

3) Store initial DB and Redis creds via CLI (replace placeholders)
- vault kv put secret/data/dev/postgres/app-creds username=app_user password=<strong-password>
- vault kv put secret/data/dev/postgres/ci-creds username=ci_user password=<strong-password>
- vault kv put secret/data/dev/redis/auth auth_token=<redis_auth_token>

4) CI integration
- Create a Vault AppRole ID and SecretID for 'ci-backend-role-dev' and store them in GitHub Actions as secrets: VAULT_ROLE_ID, VAULT_SECRET_ID. Prefer OIDC later.
- CI job should use vault login -method=approle role_id=$VAULT_ROLE_ID secret_id=$VAULT_SECRET_ID to obtain a token and then read secrets.

Security notes:
- Rotate transit keys periodically (schedule) and create new version for signing.
- Disable root tokens post-bootstrap.
- In production, use HCP Vault or Vault HA cluster with secure storage.

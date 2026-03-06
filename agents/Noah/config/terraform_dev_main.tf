# Terraform skeleton for dev environment: RDS Postgres, ElastiCache Redis, Vault (EC2) and Vault config via vault provider.
# DECISIONS (so what):
# - Cloud: AWS chosen for existing infra familiarity and available managed services (RDS / ElastiCache). Reversible: modules abstracted.
# - Vault will be provisioned on a single small EC2 for dev (non-production). Use Terraform Vault provider to configure PKI/Transit and KV secrets.
# - CI auth: Use Vault's AppRole + GitHub OIDC recommended. We create a Vault role 'ci-backend-role-dev' mapped to limited paths.
# NOTE: replace <...> variables with real values in terraform.tfvars or env.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    vault = {
      source = "hashicorp/vault"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  # Credentials via env / shared config
}

provider "vault" {
  address = var.vault_addr
  # authentication planned to be via root token for bootstrap only — rotate after init.
  token = var.vault_root_token
}

# --- Networking ---
resource "aws_vpc" "dev" {
  cidr_block = "10.10.0.0/16"
  tags = { Name = "dev-vpc" environment = "dev" owner = "backend" }
}

resource "aws_subnet" "private" {
  count = 2
  vpc_id = aws_vpc.dev.id
  cidr_block = cidrsubnet(aws_vpc.dev.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = false
  tags = { Name = "dev-private-${count.index}" environment = "dev" owner = "backend" }
}

data "aws_availability_zones" "available" {}

# Security groups: minimal ingress
resource "aws_security_group" "db_sg" {
  name        = "dev-db-sg"
  description = "Allow app and CI runners to connect to DB"
  vpc_id      = aws_vpc.dev.id
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.ci_runner_cidr, var.dev_app_cidr]
  }
  egress { from_port = 0 to_port = 0 protocol = "-1" cidr_blocks = ["0.0.0.0/0"] }
  tags = { environment = "dev" owner = "backend" }
}

resource "aws_security_group" "redis_sg" {
  name        = "dev-redis-sg"
  description = "Allow app and CI runners to connect to Redis TLS port"
  vpc_id      = aws_vpc.dev.id
  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = [var.ci_runner_cidr, var.dev_app_cidr]
  }
  egress { from_port = 0 to_port = 0 protocol = "-1" cidr_blocks = ["0.0.0.0/0"] }
  tags = { environment = "dev" owner = "backend" }
}

# --- Postgres (RDS) ---
resource "aws_db_subnet_group" "dev" {
  name       = "dev-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id
  tags = { environment = "dev" owner = "backend" }
}

resource "aws_db_instance" "postgres" {
  identifier = "dev-postgres"
  engine = "postgres"
  engine_version = "13"
  instance_class = "db.t3.micro"
  username = var.postgres_master_user
  password = var.postgres_master_password
  allocated_storage = 20
  db_subnet_group_name = aws_db_subnet_group.dev.name
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  skip_final_snapshot = true
  tags = { environment = "dev" owner = "backend" }
}

# Create CI test DB within the same instance (best for dev cost) via aws_db_instance does not create separate DB names; use null_resource to run SQL during provisioning (requires provisioner)
resource "null_resource" "create_ci_db" {
  provisioner "local-exec" {
    command = "PGPASSWORD='${var.postgres_master_password}' psql -h ${aws_db_instance.postgres.address} -U ${var.postgres_master_user} -c 'CREATE DATABASE ci_test;'"
  }
  depends_on = [aws_db_instance.postgres]
}

# --- ElastiCache Redis (single-node for dev) ---
resource "aws_elasticache_subnet_group" "dev" {
  name       = "dev-redis-subnet-group"
  subnet_ids = aws_subnet.private[*].id
  tags = { environment = "dev" owner = "backend" }
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id          = "dev-redis"
  replication_group_description = "Dev redis for refresh tokens and rate-limiter"
  node_type                     = "cache.t3.micro"
  number_cache_clusters         = 1
  automatic_failover_enabled    = false
  subnet_group_name             = aws_elasticache_subnet_group.dev.name
  security_group_ids            = [aws_security_group.redis_sg.id]
  transit_encryption_enabled   = true
  at_rest_encryption_enabled    = true
  auth_token                    = random_password.redis_auth.result
  tags = { environment = "dev" owner = "backend" }
}

resource "random_password" "redis_auth" {
  length = 32
  override_characters = "@#%^-_+="
}

# --- Vault Bootstrap on EC2 (dev only) ---
resource "aws_instance" "vault" {
  ami           = var.vault_ami
  instance_type = "t3.small"
  subnet_id     = aws_subnet.private[0].id
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  tags = { Name = "vault-dev" environment = "dev" owner = "backend" }

  user_data = <<-EOF
              #!/bin/bash
              # Install and run Vault in dev mode is NOT for production; this is bootstrap for dev.
              # In prod, use HCP Vault or HA cluster.
              apt-get update -y
              apt-get install -y unzip
              curl -sSL https://releases.hashicorp.com/vault/1.13.3/vault_1.13.3_linux_amd64.zip -o /tmp/vault.zip
              unzip /tmp/vault.zip -d /usr/local/bin/
              mkdir -p /etc/vault
              cat > /etc/vault/config.hcl <<VAULTCFG
              listener "tcp" {
                address = "0.0.0.0:8200"
                tls_disable = 1
              }
              storage "file" { path = "/opt/vault/data" }
              ui = true
              VAULTCFG
              vault server -config=/etc/vault/config.hcl &
              EOF

  depends_on = [aws_vpc.dev]
}

# --- Vault configuration via Terraform Vault provider (bootstrap requires vault provider token) ---
# KV paths, Transit, PKI, policies for app and CI are created below using the vault provider.

resource "vault_mount" "kv_dev" {
  path = "secret"
  type = "kv"
  description = "KV for dev secrets"
}

resource "vault_mount" "transit" {
  path = "transit"
  type = "transit"
}

resource "vault_transit_key" "signing" {
  name = "jwt-signing-key"
  type = "rsa-2048"
  exportable = false
  deletion_allowed = true
}

resource "vault_pki_secret_backend" "dev_pki" {
  path = "pki-dev"
  max_lease_ttl = "87600h"
}

# Policies
resource "vault_policy" "app_policy" {
  name = "app-policy-dev"
  policy = <<EOP
path "secret/data/dev/postgres/*" {
  capabilities = ["read"]
}
path "transit/sign/jwt-signing-key" {
  capabilities = ["update"]
}
EOP
}

resource "vault_policy" "ci_policy" {
  name = "ci-policy-dev"
  policy = <<EOP
path "secret/data/dev/*" {
  capabilities = ["read"]
}
path "transit/keys/jwt-signing-key" {
  capabilities = ["read"]
}
EOP
}

# AppRole for CI: least-privileged
resource "vault_auth_backend" "approle" {
  type = "approle"
}

resource "vault_approle_auth_backend_role" "ci_role" {
  backend = vault_auth_backend.approle.path
  role_name = "ci-backend-role-dev"
  token_policies = [vault_policy.ci_policy.name]
  token_ttl = "1h"
  token_max_ttl = "4h"
}

# Store Redis auth token and DB creds in KV (no plaintext here; we instruct to rotate/replace in prod)
resource "vault_kv_secret_v2" "postgres_app_creds" {
  mount = vault_mount.kv_dev.path
  name = "dev/postgres/app-creds"
  data_json = jsonencode({
    username = "app_user",
    password = "REPLACE_WITH_MANAGED_USER_PASSWORD"
  })
  depends_on = [aws_db_instance.postgres]
}

resource "vault_kv_secret_v2" "postgres_ci_creds" {
  mount = vault_mount.kv_dev.path
  name = "dev/postgres/ci-creds"
  data_json = jsonencode({
    username = "ci_user",
    password = "REPLACE_WITH_MANAGED_CI_PASSWORD"
  })
}

resource "vault_kv_secret_v2" "redis_auth" {
  mount = vault_mount.kv_dev.path
  name = "dev/redis/auth"
  data_json = jsonencode({
    auth_token = random_password.redis_auth.result
  })
  depends_on = [aws_elasticache_replication_group.redis]
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.address
}

output "redis_endpoint" {
  value = aws_elasticache_replication_group.redis.primary_endpoint_address
}

output "vault_addr" {
  value = "http://${aws_instance.vault.public_ip}:8200"
}

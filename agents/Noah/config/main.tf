terraform {
  required_version = ">= 1.0"
}

provider "aws" {
  region = var.aws_region
}

# Postgres (RDS)
resource "aws_db_subnet_group" "staging" {
  name       = "staging-db-subnet-group"
  subnet_ids = var.subnet_ids
  tags = { Name = "staging-db-subnet-group" }
}

resource "aws_db_instance" "postgres" {
  identifier             = "staging-postgres"
  engine                 = "postgres"
  engine_version         = var.postgres_version
  instance_class         = var.postgres_instance_class
  allocated_storage      = var.postgres_allocated_storage
  name                   = var.db_name
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.staging.name
  skip_final_snapshot    = true
  publicly_accessible    = false
  vpc_security_group_ids = [var.db_security_group_id]
  tags = { env = "staging" }
}

# Redis (ElastiCache)
resource "aws_elasticache_subnet_group" "staging" {
  name       = "staging-redis-subnet-group"
  subnet_ids = var.subnet_ids
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id          = "staging-redis"
  replication_group_description = "Staging Redis cluster"
  node_type                     = var.redis_node_type
  number_cache_clusters         = var.redis_cluster_size
  engine                        = "redis"
  automatic_failover_enabled    = false
  parameter_group_name          = var.redis_parameter_group
  subnet_group_name             = aws_elasticache_subnet_group.staging.name
  security_group_ids            = [var.redis_security_group_id]
  tags = { env = "staging" }
}

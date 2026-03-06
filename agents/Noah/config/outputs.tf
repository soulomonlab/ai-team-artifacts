output "pg_dev_endpoint" {
  value = aws_db_instance.dev_pg.endpoint
}

output "pg_ci_endpoint" {
  value = aws_db_instance.ci_test_pg.endpoint
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.redis.cache_nodes[0].address
}

variable "aws_region" { type = string default = "us-east-1" }
variable "vault_addr" { type = string default = "http://127.0.0.1:8200" }
variable "vault_root_token" { type = string default = "REPLACE_ROOT_TOKEN" }
variable "postgres_master_user" { type = string default = "postgres" }
variable "postgres_master_password" { type = string default = "REPLACE_MASTER_PW" }
variable "ci_runner_cidr" { type = string default = "10.20.0.0/16" }
variable "dev_app_cidr" { type = string default = "10.10.0.0/16" }
variable "vault_ami" { type = string default = "ami-0c94855ba95c71c99" }

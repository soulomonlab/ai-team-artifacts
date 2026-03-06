variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "availability_zone" {
  type    = string
  default = "us-east-1a"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "db_instance_class" {
  type    = string
  default = "db.t3.micro"
}

variable "db_name" { type = string; default = "mvpdb" }
variable "db_user" { type = string; default = "mvpuser" }
variable "db_password" { type = string; default = "changeme" }

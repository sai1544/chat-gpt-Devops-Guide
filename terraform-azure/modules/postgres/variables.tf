variable "postgres_name" {}
variable "resource_group_name" {}
variable "location" {}
variable "admin_user" {}
variable "admin_password" {
  sensitive = true
}


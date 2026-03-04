variable "location" {}
variable "resource_group_name" {}
variable "acr_name" {}
variable "aks_name" {}
variable "postgres_name" {}
variable "db_admin_user" {}
variable "db_admin_password" {
  sensitive = true
}


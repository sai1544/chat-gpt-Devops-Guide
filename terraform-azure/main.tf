module "resource_group" {
  source   = "./modules/resource-group"
  name     = var.resource_group_name
  location = var.location
}

module "acr" {
  source              = "./modules/acr"
  acr_name            = var.acr_name
  resource_group_name = module.resource_group.name
  location            = var.location
}

module "aks" {
  source              = "./modules/aks"
  aks_name            = var.aks_name
  resource_group_name = module.resource_group.name
  location            = var.location
}

module "postgres" {
  source              = "./modules/postgres"
  postgres_name       = var.postgres_name
  resource_group_name = module.resource_group.name
  location            = var.location
  admin_user          = var.db_admin_user
  admin_password      = var.db_admin_password
}


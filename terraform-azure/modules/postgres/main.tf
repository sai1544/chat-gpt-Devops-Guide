resource "azurerm_postgresql_flexible_server" "this" {
  name                   = var.postgres_name
  resource_group_name    = var.resource_group_name
  location               = var.location
  version                = "14"
  administrator_login    = var.admin_user
  administrator_password = var.admin_password
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
}


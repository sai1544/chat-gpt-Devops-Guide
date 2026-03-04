terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "tfstateaccount8672"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}


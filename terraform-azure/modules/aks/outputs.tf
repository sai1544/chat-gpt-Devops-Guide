output "kube_admin_config" {
  value     = azurerm_kubernetes_cluster.this.kube_admin_config_raw
  sensitive = true
}


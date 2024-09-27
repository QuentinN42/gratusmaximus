variable "name" {
  type = string
}

resource "kubernetes_namespace" "ns" {
  metadata {
    name = var.name
    labels = {
      "app.kubernetes.io/managed-by" = "terraform"
      "app.kubernetes.io/name"       = var.name
    }
  }
}

output "name" {
  value = kubernetes_namespace.ns.metadata[0].name
}

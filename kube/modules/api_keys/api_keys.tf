variable "ns" {
  type = string
}

variable "reqs" {
  type = set(string)
}

variable "kube_version" {
  type = string
}

locals {
  name = "keyprovisioner"
  labels = {
    "app.kubernetes.io/managed-by" = "terraform"
    "app.kubernetes.io/name"       = local.name
  }
}

resource "kubernetes_role" "this" {
  metadata {
    name      = local.name
    namespace = var.ns
    labels    = local.labels
  }

  rule {
    api_groups = [""]
    resources  = ["secrets"]
    verbs      = ["list", "get", "patch", "create"]
  }

  rule {
    api_groups = [""]
    resources  = ["pods"]
    verbs      = ["list", "get"]
  }
  rule {
    api_groups = [""]
    resources  = ["pods/exec"]
    verbs      = ["create"]
  }
}

resource "kubernetes_service_account" "this" {
  metadata {
    name      = local.name
    namespace = var.ns
    labels    = local.labels
  }

  automount_service_account_token = true
}

resource "kubernetes_role_binding" "this" {
  metadata {
    name      = local.name
    namespace = var.ns
    labels    = local.labels
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = kubernetes_role.this.metadata[0].name
  }
  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.this.metadata[0].name
    namespace = var.ns
  }
}

resource "kubernetes_job" "this" {
  metadata {
    name      = local.name
    namespace = var.ns
    labels    = local.labels
  }

  spec {
    template {
      metadata {
        name   = local.name
        labels = local.labels
      }

      spec {
        restart_policy       = "Never"
        service_account_name = kubernetes_service_account.this.metadata[0].name

        container {
          name    = local.name
          image   = "bitnami/kubectl:${var.kube_version}"
          command = ["bash", "-c", file("${path.module}/keyprovisioner.sh")]

          env {
            name  = "KEYS"
            value = join("\n", var.reqs)
          }
        }
      }
    }
    backoff_limit = 4
  }
  wait_for_completion = true
  timeouts {
    create = "2m"
    update = "2m"
  }
}

variable "image" {
  type = string
}

variable "ns" {
  type = string
}

variable "database_url" {
  type = string
}

variable "host" {
  type = string
}

locals {
  name = "maximus"
  labels = {
    "app.kubernetes.io/managed-by" = "terraform"
    "app.kubernetes.io/name"       = local.name
  }
  port = 8080
}

resource "kubernetes_deployment_v1" "deployment" {
  lifecycle {
    ignore_changes = [
      spec[0].replicas,
      spec[0].template[0].metadata[0].annotations["kubectl.kubernetes.io/restartedAt"]
    ]
  }

  metadata {
    name      = local.name
    namespace = var.ns
    labels    = local.labels
  }

  spec {
    replicas = 2

    selector {
      match_labels = local.labels
    }

    strategy {
      type = "RollingUpdate"
      rolling_update {
        max_surge       = "100%"
        max_unavailable = "50%"
      }
    }

    template {
      metadata {
        name   = local.name
        labels = local.labels
      }

      spec {
        termination_grace_period_seconds = 5

        container {
          name = local.name

          image             = var.image
          image_pull_policy = "Always"

          resources {
            limits = {
              cpu    = 1
              memory = "512Mi"
            }
            requests = {
              cpu    = 1
              memory = "512Mi"
            }
          }

          readiness_probe {
            http_get {
              path = "/health"
              port = local.port
            }

            initial_delay_seconds = 5
            period_seconds        = 5
            failure_threshold     = 5
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = local.port
            }

            initial_delay_seconds = 5
            period_seconds        = 5
            failure_threshold     = 5
          }

          env {
            name  = "PORT"
            value = local.port
          }

          env {
            name  = "DATABASE_URL"
            value = var.database_url
          }

          port {
            name           = "http"
            container_port = local.port
            protocol       = "TCP"
          }

          security_context {
            allow_privilege_escalation = false
            privileged                 = false
            run_as_non_root            = true
            run_as_user                = 1000
            run_as_group               = 1000
          }
        }

        security_context {
          run_as_non_root        = true
          run_as_user            = 1000
          run_as_group           = 1000
          fs_group               = 1000
          fs_group_change_policy = "Always"
        }
      }
    }
  }
}

resource "kubernetes_service" "svc" {
  metadata {
    name      = local.name
    namespace = var.ns
    labels    = local.labels
  }
  spec {
    selector = local.labels

    port {
      name        = "http"
      port        = 80
      target_port = local.port
    }
  }
}

resource "kubernetes_ingress_v1" "ingress" {
  metadata {
    name      = "ingress"
    namespace = var.ns
    labels    = local.labels
    annotations = {
      "cert-manager.io/cluster-issuer"   = "letsencrypt-issuer"
      "kubernetes.io/ingress.allow-http" = "true"
    }
  }

  spec {
    ingress_class_name = "nginx"

    rule {
      host = var.host
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.svc.metadata[0].name
              port {
                name = "http"
              }
            }
          }
        }
      }
    }

    tls {
      hosts = [
        var.host
      ]
      secret_name = "tls-${local.name}"
    }
  }
}

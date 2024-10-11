variable "ns" {
  type = string
}

variable "storage_class_name" {
  type    = string
  default = null
}

locals {
  name = "psql"
  labels = {
    "app.kubernetes.io/managed-by" = "terraform"
    "app.kubernetes.io/name"       = local.name
  }
  port = 5432
  pg = {
    db   = "postgres"
    user = "postgres"
  }
}

resource "kubernetes_persistent_volume_claim" "this" {
  metadata {
    name      = local.name
    namespace = var.ns

    labels = local.labels
  }

  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "5Gi"
      }
    }

    storage_class_name = var.storage_class_name
  }
}

resource "random_password" "password" {
  length  = 64
  special = false
}

resource "kubernetes_deployment_v1" "deployment" {
  lifecycle {
    ignore_changes = [
      spec[0].template[0].metadata[0].annotations["kubectl.kubernetes.io/restartedAt"]
    ]
  }

  metadata {
    name      = local.name
    namespace = var.ns
    labels    = local.labels
  }

  spec {
    replicas = 1

    selector {
      match_labels = local.labels
    }

    strategy {
      type = "Recreate"
    }

    template {
      metadata {
        name   = local.name
        labels = local.labels
      }

      spec {
        termination_grace_period_seconds = 5

        volume {
          name = local.name
          persistent_volume_claim {
            claim_name = local.name
          }
        }

        container {
          name = local.name

          volume_mount {
            mount_path = "/pgdata"
            name       = local.name
            read_only  = false
          }

          image             = "postgres:13.9"
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
            exec {
              command = ["pg_isready", "-U", local.pg.user, "-d", local.pg.db]
            }

            initial_delay_seconds = 5
            period_seconds        = 5
            failure_threshold     = 5
          }

          liveness_probe {
            exec {
              command = ["pg_isready", "-U", local.pg.user, "-d", local.pg.db]
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
            name  = "POSTGRES_DB"
            value = local.pg.db
          }
          env {
            name  = "POSTGRES_USER"
            value = local.pg.user
          }
          env {
            name  = "POSTGRES_PASSWORD"
            value = random_password.password.result
          }
          env {
            name  = "PGDATA"
            value = "/pgdata/data"
          }

          port {
            name           = "http"
            container_port = local.port
            protocol       = "TCP"
          }
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
      port        = local.port
      target_port = local.port
    }
  }
}

output "database_url" {
  value = "postgresql://${local.pg.user}:${random_password.password.result}@${kubernetes_service.svc.metadata.0.name}.${var.ns}.svc.cluster.local:${local.port}/${local.pg.db}"
}

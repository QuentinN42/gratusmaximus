variable "ns" {
  type = string
}

variable "hash" {
  type = string
}

variable "gratters" {
  type = set(string)
}

variable "maximus_url" {
  type = string
}

locals {
  labels = {
    for k in var.gratters : k => {
      "app.kubernetes.io/managed-by" = "terraform"
      "app.kubernetes.io/name"       = k
    }
  }
}

resource "kubernetes_cron_job_v1" "this" {
  for_each = local.labels

  metadata {
    namespace = var.ns
    name      = each.key
    labels    = each.value
  }

  spec {
    concurrency_policy            = "Replace"
    failed_jobs_history_limit     = 5
    schedule                      = "0 8 * * *"
    starting_deadline_seconds     = 10
    successful_jobs_history_limit = 10

    job_template {
      metadata {
        name   = each.key
        labels = each.value
      }

      spec {
        backoff_limit              = 2
        ttl_seconds_after_finished = 10
        template {
          metadata {
            name   = each.key
            labels = each.value
          }

          spec {
            container {
              name  = each.key
              image = "quentinn42/gratusmaximus:${each.key}-${var.hash}"

              env {
                name  = "MAXIMUS_URL"
                value = var.maximus_url
              }

              env {
                name = "MAXIMUS_API_KEY"
                value_from {
                  secret_key_ref {
                    name = each.key
                    key  = "key"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

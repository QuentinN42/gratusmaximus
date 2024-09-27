terraform {
  required_version = ">= 1.0"

  backend "kubernetes" {
    secret_suffix = "gratusmaximus"
  }

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.32.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.1.0"
    }
  }
}

variable "k8s_config_path" {
  type = string
}

variable "k8s_config_context" {
  type = string
}

provider "kubernetes" {}

provider "random" {}

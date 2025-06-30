terraform {
  # Require Terraform v1.3.0 or higher for modern features and compatibility
  required_version = ">= 1.3.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"  # Ensures compatibility with newer AWS resources and syntax
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.20.0" # Supports major Kubernetes API changes
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.1.0"
    }

    local = {
      source  = "hashicorp/local"
      version = "~> 2.1.0"
    }

    null = {
      source  = "hashicorp/null"
      version = "~> 3.1.0"
    }

    cloudinit = {
      source  = "hashicorp/cloudinit"
      version = "~> 2.2.0" # Be mindful of locked versions; run 'terraform init -upgrade' if needed
    }
  }
}

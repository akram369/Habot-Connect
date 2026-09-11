# ==============================================================================
# Habot Connect FZCO — Infrastructure as Code (IaC)
# Module: Terraform Core & Google Cloud Provider Version Locking
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.20.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.20.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6.0"
    }
  }

  # Production/Staging Remote State Backend Configuration
  # backend "gcs" {
  #   bucket = "habotconnect-terraform-state-staging"
  #   prefix = "staging/data-platform"
  # }
}

provider "google" {
  project = var.google_cloud_project_identifier
  region  = var.google_cloud_primary_region
}

provider "google-beta" {
  project = var.google_cloud_project_identifier
  region  = var.google_cloud_primary_region
}

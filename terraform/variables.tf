# ==============================================================================
# Habot Connect FZCO — Infrastructure as Code (IaC)
# Module: Input Variable Definitions with Strict Types and Validations
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# ==============================================================================

variable "google_cloud_project_identifier" {
  type        = string
  description = "The globally unique identifier of the Google Cloud Platform project hosting the staging infrastructure."
  default     = "habotconnect-staging-2026"

  validation {
    condition     = can(regex("^[a-z0-9-]{6,30}$", var.google_cloud_project_identifier))
    error_message = "The project identifier must be between 6 and 30 lowercase alphanumeric characters or hyphens."
  }
}

variable "google_cloud_primary_region" {
  type        = string
  description = "The primary Google Cloud Platform geographical region for resource provisioning, compliant with UAE data sovereignty."
  default     = "me-central1"
}

variable "google_cloud_secondary_region" {
  type        = string
  description = "The secondary Google Cloud Platform geographical region for disaster recovery and multi-regional redundancy."
  default     = "europe-west1"
}

variable "deployment_environment_name" {
  type        = string
  description = "The operational deployment environment tier (strictly development, staging, or production)."
  default     = "staging"

  validation {
    condition     = contains(["development", "staging", "production"], var.deployment_environment_name)
    error_message = "The environment name must strictly be one of: development, staging, production."
  }
}

variable "data_retention_days_raw_landing" {
  type        = number
  description = "The duration in days before uncompressed objects in the D0 Raw Landing Google Cloud Storage bucket are permanently deleted."
  default     = 90

  validation {
    condition     = var.data_retention_days_raw_landing >= 30 && var.data_retention_days_raw_landing <= 365
    error_message = "The raw landing data retention period must be configured between 30 and 365 days."
  }
}

variable "bigquery_table_expiration_days_staged" {
  type        = number
  description = "The duration in days before partition tables in the D1 Staged Google BigQuery dataset expire."
  default     = 180

  validation {
    condition     = var.bigquery_table_expiration_days_staged >= 60 && var.bigquery_table_expiration_days_staged <= 730
    error_message = "The staged dataset expiration period must be configured between 60 and 730 days."
  }
}

variable "authorized_compliance_officer_group_email" {
  type        = string
  description = "The Google Workspace directory group email address granted full access across all regional rows for compliance auditing."
  default     = "compliance-officers@habotconnect.internal"
}

variable "authorized_learning_support_assistant_group_email" {
  type        = string
  description = "The Google Workspace directory group email address representing active Learning Support Assistants subject to Row-Level Security."
  default     = "learning-support-assistants@habotconnect.internal"
}

variable "data_ingestion_service_account_identifier" {
  type        = string
  description = "The service account identifier dedicated to streaming and batch ingestion into the D0 Raw Landing bucket."
  default     = "sa-data-ingestion-staging"
}

variable "data_analytics_service_account_identifier" {
  type        = string
  description = "The service account identifier dedicated to running analytics transformations from D0 Raw Landing to D1 Staged Enforced."
  default     = "sa-analytics-pipeline-staging"
}

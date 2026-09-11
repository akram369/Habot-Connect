# ==============================================================================
# Habot Connect FZCO — Infrastructure as Code (IaC)
# Module: Terraform Outputs with Structural Resource Identifiers
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# ==============================================================================

output "gcs_d0_raw_landing_bucket_name" {
  description = "The globally unique bucket name of the D0 Raw Landing Google Cloud Storage bucket."
  value       = google_storage_bucket.d0_raw_landing_bucket.name
}

output "gcs_d0_raw_landing_bucket_url" {
  description = "The gs:// uniform resource identifier for the D0 Raw Landing bucket."
  value       = google_storage_bucket.d0_raw_landing_bucket.url
}

output "gcs_audit_logging_bucket_name" {
  description = "The bucket name dedicated to storing immutable storage audit access logs."
  value       = google_storage_bucket.gcs_audit_logging_bucket.name
}

output "bigquery_d1_staged_dataset_identifier" {
  description = "The unique identifier of the D1 Staged and Enforced Google BigQuery dataset."
  value       = google_bigquery_dataset.d1_staged_enforced_dataset.dataset_id
}

output "bigquery_student_onboarding_table_identifier" {
  description = "The fully qualified BigQuery table identifier for staged student onboarding data."
  value       = "${var.google_cloud_project_identifier}.${google_bigquery_dataset.d1_staged_enforced_dataset.dataset_id}.${google_bigquery_table.student_onboarding_staged_table.table_id}"
}

output "cloud_kms_key_ring_identifier" {
  description = "The Google Cloud Key Management Service Keyring hosting Customer-Managed Encryption Keys."
  value       = google_kms_key_ring.staging_encryption_key_ring.id
}

output "data_ingestion_service_account_email_address" {
  description = "The electronic mail address of the Ingestion Pipeline Service Account."
  value       = google_service_account.data_ingestion_service_account.email
}

output "data_analytics_service_account_email_address" {
  description = "The electronic mail address of the Analytics Transformation Service Account."
  value       = google_service_account.data_analytics_service_account.email
}

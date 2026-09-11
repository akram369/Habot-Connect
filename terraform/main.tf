# ==============================================================================
# Habot Connect FZCO — Infrastructure as Code (IaC)
# Module: Secure Staging Provisioning (Google Cloud Storage & BigQuery)
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# Date: September 2026
# ==============================================================================

# Random suffix generator for globally unique storage resource identifiers
resource "random_id" "storage_resource_suffix" {
  byte_length = 4
}

# ------------------------------------------------------------------------------
# Google Cloud Key Management Service (Cloud KMS) — Customer-Managed Keys (CMEK)
# ------------------------------------------------------------------------------
resource "google_kms_key_ring" "staging_encryption_key_ring" {
  name     = "habotconnect-staging-keyring-${var.deployment_environment_name}"
  location = var.google_cloud_primary_region
  project  = var.google_cloud_project_identifier
}

resource "google_kms_crypto_key" "storage_encryption_cryptokey" {
  name            = "habotconnect-storage-encryption-key"
  key_ring        = google_kms_key_ring.staging_encryption_key_ring.id
  rotation_period = "7776000s" # 90 days automatic rotation

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_kms_crypto_key" "bigquery_encryption_cryptokey" {
  name            = "habotconnect-bigquery-encryption-key"
  key_ring        = google_kms_key_ring.staging_encryption_key_ring.id
  rotation_period = "7776000s" # 90 days automatic rotation

  lifecycle {
    prevent_destroy = true
  }
}

# Grant Storage Service Agent permission to encrypt and decrypt using CMEK
data "google_storage_project_service_account" "default_storage_service_agent" {
  project = var.google_cloud_project_identifier
}

resource "google_kms_crypto_key_iam_member" "storage_service_agent_kms_binding" {
  crypto_key_id = google_kms_crypto_key.storage_encryption_cryptokey.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:${data.google_storage_project_service_account.default_storage_service_agent.email_address}"
}

# Grant BigQuery Service Agent permission to encrypt and decrypt using CMEK
data "google_bigquery_default_service_account" "default_bigquery_service_agent" {
  project = var.google_cloud_project_identifier
}

resource "google_kms_crypto_key_iam_member" "bigquery_service_agent_kms_binding" {
  crypto_key_id = google_kms_crypto_key.bigquery_encryption_cryptokey.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:${data.google_bigquery_default_service_account.default_bigquery_service_agent.email}"
}

# ------------------------------------------------------------------------------
# Google Cloud Service Accounts (Least Privilege Architecture)
# ------------------------------------------------------------------------------
resource "google_service_account" "data_ingestion_service_account" {
  account_id   = var.data_ingestion_service_account_identifier
  display_name = "HabotConnect Ingestion Pipeline Service Account (${var.deployment_environment_name})"
  description  = "Dedicated service account for landing raw student onboarding JSON payloads into D0 Storage."
  project      = var.google_cloud_project_identifier
}

resource "google_service_account" "data_analytics_service_account" {
  account_id   = var.data_analytics_service_account_identifier
  display_name = "HabotConnect Analytics Transformation Service Account (${var.deployment_environment_name})"
  description  = "Dedicated service account for ETL transformation from D0 Raw Landing to D1 Staged BigQuery."
  project      = var.google_cloud_project_identifier
}

# ------------------------------------------------------------------------------
# Audit Logging Bucket (Destination for GCS Access and Storage Logs)
# ------------------------------------------------------------------------------
resource "google_storage_bucket" "gcs_audit_logging_bucket" {
  name                        = "habotconnect-audit-logs-${var.deployment_environment_name}-${random_id.storage_resource_suffix.hex}"
  location                    = var.google_cloud_primary_region
  project                     = var.google_cloud_project_identifier
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = true
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.storage_encryption_cryptokey.id
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 365 # Retain audit logs for 1 continuous year
    }
  }
}

# ------------------------------------------------------------------------------
# Task 1.1: Google Cloud Storage Raw Landing Bucket (D0 Raw Landing)
# ------------------------------------------------------------------------------
resource "google_storage_bucket" "d0_raw_landing_bucket" {
  name                        = "habotconnect-d0-raw-landing-${var.deployment_environment_name}-${random_id.storage_resource_suffix.hex}"
  location                    = var.google_cloud_primary_region
  project                     = var.google_cloud_project_identifier
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = true
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.storage_encryption_cryptokey.id
  }

  logging {
    log_bucket        = google_storage_bucket.gcs_audit_logging_bucket.name
    log_object_prefix = "storage-access-logs/d0-raw-landing/"
  }

  # Cost Optimization & Mistake-Proofing Retention Lifecycle Rules
  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
    condition {
      age        = 30
      with_state = "LIVE"
    }
  }

  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
    condition {
      age        = 60
      with_state = "LIVE"
    }
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age        = var.data_retention_days_raw_landing
      with_state = "LIVE"
    }
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      days_since_noncurrent_time = 14
      with_state                 = "ARCHIVED"
    }
  }

  labels = {
    organization        = "habotconnect"
    environment         = var.deployment_environment_name
    data_classification = "confidential-raw-landing"
    managed_by          = "terraform"
  }

  depends_on = [
    google_kms_crypto_key_iam_member.storage_service_agent_kms_binding
  ]
}

# ------------------------------------------------------------------------------
# Task 1.2: Strict IAM Conditions & Least Privilege for D0 Raw Landing
# ------------------------------------------------------------------------------
# Restrict Ingestion Service Account to objectCreator on raw landing paths
resource "google_storage_bucket_iam_member" "ingestion_service_account_creator_binding" {
  bucket = google_storage_bucket.d0_raw_landing_bucket.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.data_ingestion_service_account.email}"

  condition {
    title       = "EnforceIngestionObjectPrefixCondition"
    description = "Mistake-proofing condition: Ingestion Service Account can only write objects to the raw onboarding path."
    expression  = "resource.name.startsWith('projects/_/buckets/${google_storage_bucket.d0_raw_landing_bucket.name}/objects/student_onboarding_raw/')"
  }
}

# Restrict Analytics Pipeline Service Account to objectViewer on raw landing paths
resource "google_storage_bucket_iam_member" "analytics_service_account_viewer_binding" {
  bucket = google_storage_bucket.d0_raw_landing_bucket.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.data_analytics_service_account.email}"

  condition {
    title       = "EnforceAnalyticsReadCondition"
    description = "Analytics pipeline service account can only inspect verified raw ingestion batches."
    expression  = "resource.name.startsWith('projects/_/buckets/${google_storage_bucket.d0_raw_landing_bucket.name}/objects/student_onboarding_raw/')"
  }
}

# ------------------------------------------------------------------------------
# Task 1.3: Google BigQuery Dataset (D1 Staged/Enforced)
# ------------------------------------------------------------------------------
resource "google_bigquery_dataset" "d1_staged_enforced_dataset" {
  dataset_id                  = "habotconnect_d1_staged_enforced"
  friendly_name               = "HabotConnect Staged and Enforced Analytics Dataset (${var.deployment_environment_name})"
  description                 = "Poka-Yoke staged data warehouse containing cleansed, DCYN-validated student profiles for analytical matching."
  location                    = var.google_cloud_primary_region
  project                     = var.google_cloud_project_identifier
  default_table_expiration_ms = var.bigquery_table_expiration_days_staged * 86400 * 1000

  default_encryption_configuration {
    kms_key_name = google_kms_crypto_key.bigquery_encryption_cryptokey.id
  }

  labels = {
    organization        = "habotconnect"
    environment         = var.deployment_environment_name
    data_classification = "confidential-staged-enforced"
    managed_by          = "terraform"
  }

  # Access Control List enforcing Least Privilege
  access {
    role          = "OWNER"
    user_by_email = "admin@habotconnect.internal"
  }

  access {
    role          = "WRITER"
    user_by_email = google_service_account.data_analytics_service_account.email
  }

  access {
    role           = "READER"
    group_by_email = var.authorized_compliance_officer_group_email
  }

  access {
    role           = "READER"
    group_by_email = var.authorized_learning_support_assistant_group_email
  }

  depends_on = [
    google_kms_crypto_key_iam_member.bigquery_service_agent_kms_binding
  ]
}

# ------------------------------------------------------------------------------
# Task 1.4: BigQuery Staged Table with Time Partitioning & Clustering
# ------------------------------------------------------------------------------
resource "google_bigquery_table" "student_onboarding_staged_table" {
  dataset_id          = google_bigquery_dataset.d1_staged_enforced_dataset.dataset_id
  table_id            = "student_onboarding_staged"
  project             = var.google_cloud_project_identifier
  friendly_name       = "Student Onboarding Staged Enforced Table"
  description         = "Enforced schema destination for clean student onboarding transactions validated through the DCYN library."
  deletion_protection = false

  time_partitioning {
    type  = "DAY"
    field = "ingestion_timestamp"
  }

  clustering = [
    "assigned_learning_support_assistant_identifier",
    "regional_jurisdiction"
  ]

  schema = jsonencode([
    {
      name        = "student_unique_identifier"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Globally unique Universally Unique Identifier Version 4 for the student."
    },
    {
      name        = "student_full_name"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Legal full name of the student seeking learning support."
    },
    {
      name        = "date_of_birth"
      type        = "DATE"
      mode        = "REQUIRED"
      description = "Date of birth of the student, validated between 3 and 18 years of age."
    },
    {
      name        = "parent_full_name"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Legal full name of the primary parent or guardian."
    },
    {
      name        = "parent_email_address"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Verified electronic mail address of the primary parent."
    },
    {
      name        = "parent_phone_number"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "International E.164 formatted telephone number of the parent."
    },
    {
      name        = "emergency_contact_full_name"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Full legal name of the designated secondary emergency contact."
    },
    {
      name        = "emergency_contact_phone_number"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "International E.164 formatted phone number of the emergency contact."
    },
    {
      name        = "primary_learning_support_category"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Categorical neurodivergent support domain (Autism Spectrum, ADHD, Dyslexia, Speech Language)."
    },
    {
      name        = "assigned_learning_support_assistant_identifier"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Corporate electronic mail address or identifier of the assigned Learning Support Assistant."
    },
    {
      name        = "regional_jurisdiction"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Geographical educational district or municipal regulatory zone (for example: Dubai, Abu Dhabi)."
    },
    {
      name        = "dcyn_has_prior_formal_diagnosis"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN Binary: Confirmed clinical diagnosis from an accredited educational psychologist."
    },
    {
      name        = "dcyn_requires_one_on_one_support"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN Binary: Requirement for dedicated one-on-one classroom assistance."
    },
    {
      name        = "dcyn_has_individualized_education_plan"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN Binary: Active Individualized Education Plan (IEP) document verified on file."
    },
    {
      name        = "dcyn_requires_non_verbal_communication_assistance"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN Binary: Requirement for Picture Exchange Communication System or speech generation technology."
    },
    {
      name        = "dcyn_has_physical_mobility_assistance_needs"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN Binary: Physical navigation or wheelchair accessibility support requirement."
    },
    {
      name        = "dcyn_is_independently_toilet_trained"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN Binary: Child is independently trained for restroom and hygiene activities."
    },
    {
      name        = "dcyn_has_sensory_sensitivity_triggers"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN Binary: Severe sensory processing triggers (acoustic sensitivity, light sensitivity)."
    },
    {
      name        = "dcyn_parental_data_processing_consent_granted"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN Binary: Explicit parental authorization under UAE Federal Data Protection Regulations."
    },
    {
      name        = "dcyn_emergency_medical_action_plan_available"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN Binary: Certified pediatric emergency medical protocol and allergy management document."
    },
    {
      name        = "dcyn_transportation_assistance_required"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN Binary: Special vehicle or physical escort requirement during school transit."
    },
    {
      name        = "ingestion_timestamp"
      type        = "TIMESTAMP"
      mode        = "REQUIRED"
      description = "Universal Time Coordinated timestamp when the record passed the Poka-Yoke build gate."
    },
    {
      name        = "schema_version"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Enforced schema semantic version (strictly 'v1.0.0')."
    },
    {
      name        = "data_payload_sha256_hash"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Cryptographic SHA-256 digest of original raw JSON payload guaranteeing tamper-proof auditability."
    }
  ])
}

# ------------------------------------------------------------------------------
# Task 1.5: BigQuery Row-Level Security (RLS) Row Access Policies
# In Google Cloud BigQuery, Row Access Policies are enforced via SQL DDL scripts.
# Declarative specifications are maintained in: terraform/rls_policies.sql
# Policies:
#  1. lsa_assigned_students_isolation (SESSION_USER() filter on assigned LSA)
#  2. regional_coordinator_district_isolation (District mapping filter)
#  3. compliance_officer_full_audit (Unrestricted TRUE filter for legal/compliance)
# ------------------------------------------------------------------------------

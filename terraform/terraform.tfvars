# ==============================================================================
# Habot Connect FZCO — Infrastructure as Code (IaC)
# Module: Staging Environment Variable Values
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# ==============================================================================

google_cloud_project_identifier              = "habotconnect-staging-2026"
google_cloud_primary_region                  = "me-central1"
google_cloud_secondary_region                = "europe-west1"
deployment_environment_name                  = "staging"
data_retention_days_raw_landing              = 90
bigquery_table_expiration_days_staged        = 180
authorized_compliance_officer_group_email    = "compliance-officers@habotconnect.internal"
authorized_learning_support_assistant_group_email = "learning-support-assistants@habotconnect.internal"
data_ingestion_service_account_identifier    = "sa-data-ingestion-staging"
data_analytics_service_account_identifier    = "sa-analytics-pipeline-staging"

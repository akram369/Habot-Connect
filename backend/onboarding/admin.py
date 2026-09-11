# ==============================================================================
# Habot Connect FZCO — Django Admin Registration
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# ==============================================================================

from django.contrib import admin
from onboarding.models import StudentOnboardingProfile


@admin.register(StudentOnboardingProfile)
class StudentOnboardingProfileAdmin(admin.ModelAdmin):
    list_display = (
        "student_unique_identifier",
        "student_full_name",
        "primary_learning_support_category",
        "regional_jurisdiction",
        "ingestion_timestamp",
    )
    search_fields = (
        "student_unique_identifier",
        "student_full_name",
        "parent_email_address",
        "parent_full_name",
    )
    list_filter = (
        "primary_learning_support_category",
        "regional_jurisdiction",
        "dcyn_parental_data_processing_consent_granted",
    )
    readonly_fields = (
        "student_unique_identifier",
        "ingestion_timestamp",
        "data_payload_sha256_hash",
    )

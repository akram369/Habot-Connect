# ==============================================================================
# Habot Connect FZCO — Data Models
# Module: Student Onboarding Profile Database Model
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# Date: September 2026
# ==============================================================================

import uuid

from django.db import models
from django.utils import timezone


class StudentOnboardingProfile(models.Model):
    """
    Persistent model representing a fully validated student onboarding profile.
    Mirror of the Google BigQuery D1 Staged/Enforced data warehouse table.
    """

    class LearningSupportCategoryChoices(models.TextChoices):
        AUTISM_SPECTRUM_DISORDER = ("AUTISM_SPECTRUM_DISORDER", "Autism Spectrum Disorder")
        ATTENTION_DEFICIT_HYPERACTIVITY_DISORDER = (
            "ATTENTION_DEFICIT_HYPERACTIVITY_DISORDER",
            "Attention Deficit Hyperactivity Disorder",
        )
        DYSLEXIA_AND_LITERACY_DIFFICULTIES = (
            "DYSLEXIA_AND_LITERACY_DIFFICULTIES",
            "Dyslexia and Literacy Difficulties",
        )
        SPEECH_AND_LANGUAGE_IMPAIRMENT = (
            "SPEECH_AND_LANGUAGE_IMPAIRMENT",
            "Speech and Language Impairment",
        )
        GENERAL_COGNITIVE_DEVELOPMENTAL_DELAY = (
            "GENERAL_COGNITIVE_DEVELOPMENTAL_DELAY",
            "General Cognitive Developmental Delay",
        )

    class RegionalJurisdictionChoices(models.TextChoices):
        DUBAI = "DUBAI", "Dubai Educational District"
        ABU_DHABI = "ABU_DHABI", "Abu Dhabi Educational District"
        SHARJAH = "SHARJAH", "Sharjah Educational District"
        NORTHERN_EMIRATES = "NORTHERN_EMIRATES", "Northern Emirates Educational District"

    # Core Identifiers
    student_unique_identifier = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Globally unique UUIDv4 identifying the student.",
    )
    student_full_name = models.CharField(
        max_length=100, help_text="Full legal name of the student."
    )
    date_of_birth = models.DateField(
        help_text="Student date of birth (must be between 3 and 18 years old)."
    )

    # Guardian & Emergency Contact Information
    parent_full_name = models.CharField(
        max_length=100, help_text="Full legal name of the primary parent or legal guardian."
    )
    parent_email_address = models.EmailField(
        max_length=254, help_text="Verified contact email address of the parent."
    )
    parent_phone_number = models.CharField(
        max_length=20, help_text="E.164 formatted international contact number of the parent."
    )
    emergency_contact_full_name = models.CharField(
        max_length=100, help_text="Full legal name of the secondary emergency contact."
    )
    emergency_contact_phone_number = models.CharField(
        max_length=20, help_text="E.164 formatted international emergency contact number."
    )

    # Operational & Support Classifications
    primary_learning_support_category = models.CharField(
        max_length=60,
        choices=LearningSupportCategoryChoices.choices,
        help_text="Accredited diagnostic classification domain.",
    )
    assigned_learning_support_assistant_identifier = models.EmailField(
        max_length=254, help_text="Email of the assigned Learning Support Assistant."
    )
    regional_jurisdiction = models.CharField(
        max_length=50,
        choices=RegionalJurisdictionChoices.choices,
        help_text="Geographical regulatory school district.",
    )

    # Deterministic Clean Yes/No (DCYN) Binary Fields
    dcyn_has_prior_formal_diagnosis = models.BooleanField(
        default=False, help_text="DCYN: Formally certified diagnosis on record."
    )
    dcyn_requires_one_on_one_support = models.BooleanField(
        default=False, help_text="DCYN: Dedicated one-on-one LSA requirement."
    )
    dcyn_has_individualized_education_plan = models.BooleanField(
        default=False, help_text="DCYN: Active Individualized Education Plan (IEP)."
    )
    dcyn_requires_non_verbal_communication_assistance = models.BooleanField(
        default=False, help_text="DCYN: Augmentative/Alternative communication requirement."
    )
    dcyn_has_physical_mobility_assistance_needs = models.BooleanField(
        default=False, help_text="DCYN: Wheelchair or classroom mobility needs."
    )
    dcyn_is_independently_toilet_trained = models.BooleanField(
        default=False, help_text="DCYN: Bathroom independence verified."
    )
    dcyn_has_sensory_sensitivity_triggers = models.BooleanField(
        default=False, help_text="DCYN: Severe sensory sensitivity indicators."
    )
    dcyn_parental_data_processing_consent_granted = models.BooleanField(
        default=False, help_text="DCYN: Verified legal consent under UAE data privacy regulations."
    )
    dcyn_emergency_medical_action_plan_available = models.BooleanField(
        default=False, help_text="DCYN: Emergency pediatric medical action plan verified."
    )
    dcyn_transportation_assistance_required = models.BooleanField(
        default=False, help_text="DCYN: Special vehicle transit accommodations needed."
    )

    # Ingestion Audit Metadata
    ingestion_timestamp = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text="UTC timestamp of ingestion into the system.",
    )
    schema_version = models.CharField(
        max_length=10,
        default="v1.0.0",
        editable=False,
        help_text="Version of the enforced schema contract.",
    )
    data_payload_sha256_hash = models.CharField(
        max_length=64,
        editable=False,
        help_text="Cryptographic SHA-256 hash of original raw JSON payload.",
    )

    class Meta:
        db_table = "student_onboarding_profiles"
        ordering = ["-ingestion_timestamp"]
        verbose_name = "Student Onboarding Profile"
        verbose_name_plural = "Student Onboarding Profiles"

    def __str__(self) -> str:
        return (
            f"{self.student_full_name} ({self.student_unique_identifier}) - "
            f"{self.regional_jurisdiction}"
        )

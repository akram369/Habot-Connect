# ==============================================================================
# Habot Connect FZCO — Django REST Framework Serializers
# Module: Zero-Judgment Student Onboarding ModelSerializer
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# Date: September 2026
# ==============================================================================

import datetime
import hashlib
import json
import re
from typing import Any, Dict

from django.utils import timezone
from onboarding.dcyn_library import (
    DCYN_STUDENT_QUESTION_CATALOG,
    DCYNTransformer,
    DCYNValidationError,
)
from onboarding.models import StudentOnboardingProfile
from rest_framework import serializers

# International E.164 Telephone Format Regex (+ followed by 7 to 15 digits)
E164_PHONE_REGEX = re.compile(r"^\+[1-9]\d{6,14}$")

# Strict Legal Name Regex (alphabetic, spaces, hyphens, apostrophes only)
LEGAL_NAME_REGEX = re.compile(r"^[A-Za-z\s\'-]{2,100}$")

# Disposable / Temporary Email Domains Blocklist (Zero Tolerance)
DISPOSABLE_EMAIL_DOMAINS = frozenset(
    {
        "mailinator.com",
        "tempmail.com",
        "guerrillamail.com",
        "10minutemail.com",
        "throwawaymail.com",
        "sharklasers.com",
        "dispostable.com",
    }
)


class StudentOnboardingSerializer(serializers.ModelSerializer):
    """
    Poka-Yoke Enforced Serializer with exact field validation limits
    designed to eliminate 100% of human ambiguity and judgment.
    """

    dcyn_indicators = serializers.DictField(
        child=serializers.CharField(),
        required=False,
        write_only=True,
        help_text="Optional dictionary of DCYN binary evaluation questions.",
    )

    class Meta:
        model = StudentOnboardingProfile
        fields = [
            "student_unique_identifier",
            "student_full_name",
            "date_of_birth",
            "parent_full_name",
            "parent_email_address",
            "parent_phone_number",
            "emergency_contact_full_name",
            "emergency_contact_phone_number",
            "primary_learning_support_category",
            "assigned_learning_support_assistant_identifier",
            "regional_jurisdiction",
            "dcyn_has_prior_formal_diagnosis",
            "dcyn_requires_one_on_one_support",
            "dcyn_has_individualized_education_plan",
            "dcyn_requires_non_verbal_communication_assistance",
            "dcyn_has_physical_mobility_assistance_needs",
            "dcyn_is_independently_toilet_trained",
            "dcyn_has_sensory_sensitivity_triggers",
            "dcyn_parental_data_processing_consent_granted",
            "dcyn_emergency_medical_action_plan_available",
            "dcyn_transportation_assistance_required",
            "ingestion_timestamp",
            "schema_version",
            "data_payload_sha256_hash",
            "dcyn_indicators",
        ]
        read_only_fields = [
            "student_unique_identifier",
            "ingestion_timestamp",
            "schema_version",
            "data_payload_sha256_hash",
        ]

    # --------------------------------------------------------------------------
    # Field-Level Exact Limit Validations (Zero Human Discretion)
    # --------------------------------------------------------------------------

    def validate_student_full_name(self, value: str) -> str:
        trimmed = value.strip()
        if len(trimmed) < 2 or len(trimmed) > 100:
            raise serializers.ValidationError(
                f"Exact boundary violation: Name length must be between 2 and 100 "
                f"characters (received {len(trimmed)})."
            )
        if not LEGAL_NAME_REGEX.match(trimmed):
            raise serializers.ValidationError(
                "Invalid characters: Name may only contain letters, spaces, hyphens, apostrophes."
            )
        return trimmed

    def validate_date_of_birth(self, value: datetime.date) -> datetime.date:
        today = timezone.now().date()
        if value >= today:
            raise serializers.ValidationError(
                "Chronological boundary violation: Date of birth cannot be in present or future."
            )

        age_in_years = (today - value).days / 365.2425

        if age_in_years < 3.0:
            raise serializers.ValidationError(
                f"Age limit violation: Student age ({age_in_years:.2f} years) is below the "
                "minimum threshold of 3.00 years for early intervention."
            )
        if age_in_years > 18.0:
            raise serializers.ValidationError(
                f"Age limit violation: Student age ({age_in_years:.2f} years) exceeds the "
                "maximum support limit of 18.00 years."
            )
        return value

    def validate_parent_full_name(self, value: str) -> str:
        trimmed = value.strip()
        if len(trimmed) < 2 or len(trimmed) > 100:
            raise serializers.ValidationError(
                f"Exact boundary: Parent name must be 2 to 100 chars (received {len(trimmed)})."
            )
        if not LEGAL_NAME_REGEX.match(trimmed):
            raise serializers.ValidationError(
                "Invalid characters: Parent name may only contain letters, spaces, hyphens."
            )
        return trimmed

    def validate_parent_email_address(self, value: str) -> str:
        cleaned = value.strip().lower()
        domain = cleaned.split("@")[-1] if "@" in cleaned else ""
        if domain in DISPOSABLE_EMAIL_DOMAINS:
            raise serializers.ValidationError(
                f"Security policy violation: Disposable email domain '{domain}' is prohibited."
            )
        return cleaned

    def validate_parent_phone_number(self, value: str) -> str:
        cleaned = value.strip().replace(" ", "").replace("-", "")
        if not E164_PHONE_REGEX.match(cleaned):
            raise serializers.ValidationError(
                "Format violation: Parent phone must adhere to international E.164 format."
            )
        return cleaned

    def validate_emergency_contact_full_name(self, value: str) -> str:
        trimmed = value.strip()
        if len(trimmed) < 2 or len(trimmed) > 100:
            raise serializers.ValidationError(
                f"Exact boundary: Emergency name must be 2-100 chars (received {len(trimmed)})."
            )
        if not LEGAL_NAME_REGEX.match(trimmed):
            raise serializers.ValidationError(
                "Invalid characters: Emergency name may only contain letters, spaces, hyphens."
            )
        return trimmed

    def validate_emergency_contact_phone_number(self, value: str) -> str:
        cleaned = value.strip().replace(" ", "").replace("-", "")
        if not E164_PHONE_REGEX.match(cleaned):
            raise serializers.ValidationError(
                "Format violation: Emergency phone must adhere to international E.164 format."
            )
        return cleaned

    def validate_assigned_learning_support_assistant_identifier(self, value: str) -> str:
        cleaned = value.strip().lower()
        if "@" not in cleaned or "." not in cleaned:
            raise serializers.ValidationError(
                "Format violation: Assigned LSA identifier must be a valid email address."
            )
        return cleaned

    # --------------------------------------------------------------------------
    # Object-Level Cross-Field Validations & DCYN Transformation
    # --------------------------------------------------------------------------

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        parent_name = attrs.get("parent_full_name", "").strip().lower()
        emergency_name = attrs.get("emergency_contact_full_name", "").strip().lower()

        if parent_name and emergency_name and parent_name == emergency_name:
            raise serializers.ValidationError(
                {
                    "emergency_contact_full_name": (
                        "Cross-field violation: Emergency contact "
                        "must be distinct from primary parent."
                    )
                }
            )

        parent_phone = attrs.get("parent_phone_number", "").strip()
        emergency_phone = attrs.get("emergency_contact_phone_number", "").strip()

        if parent_phone and emergency_phone and parent_phone == emergency_phone:
            raise serializers.ValidationError(
                {
                    "emergency_contact_phone_number": (
                        "Cross-field violation: Emergency phone must be distinct from parent phone."
                    )
                }
            )

        raw_dcyn_container = attrs.pop("dcyn_indicators", {}) or {}

        for question_key in DCYN_STUDENT_QUESTION_CATALOG:
            field_name = f"dcyn_{question_key}"
            raw_val = raw_dcyn_container.get(question_key)
            if raw_val is None:
                raw_val = raw_dcyn_container.get(field_name)
            if raw_val is None:
                raw_val = attrs.get(field_name)

            if raw_val is None:
                raise serializers.ValidationError(
                    {
                        field_name: (
                            f"Missing mandatory DCYN indicator: '{question_key}'. "
                            "All 10 binary evaluation questions must be explicitly answered."
                        )
                    }
                )

            try:
                attrs[field_name] = DCYNTransformer.to_boolean(field_name, raw_val)
            except DCYNValidationError as err:
                raise serializers.ValidationError({field_name: str(err)})

        if not attrs.get("dcyn_parental_data_processing_consent_granted", False):
            raise serializers.ValidationError(
                {
                    "dcyn_parental_data_processing_consent_granted": (
                        "Legal compliance failure: Parental data processing consent "
                        "must be affirmatively granted (TRUE)."
                    )
                }
            )

        digest_input = json.dumps(
            {k: str(v) for k, v in attrs.items() if not k.startswith("_")},
            sort_keys=True,
        ).encode("utf-8")
        attrs["data_payload_sha256_hash"] = hashlib.sha256(digest_input).hexdigest()
        attrs["schema_version"] = "v1.0.0"
        attrs["ingestion_timestamp"] = timezone.now()

        return attrs

    # --------------------------------------------------------------------------
    # Downstream BigQuery & Pub/Sub Streaming Serializers
    # --------------------------------------------------------------------------

    def to_bigquery_row(self, instance: StudentOnboardingProfile) -> Dict[str, Any]:
        """Structures validated profile into a dictionary matching D1 Staged BigQuery table."""
        return {
            "student_unique_identifier": str(instance.student_unique_identifier),
            "student_full_name": instance.student_full_name,
            "date_of_birth": instance.date_of_birth.isoformat(),
            "parent_full_name": instance.parent_full_name,
            "parent_email_address": instance.parent_email_address,
            "parent_phone_number": instance.parent_phone_number,
            "emergency_contact_full_name": instance.emergency_contact_full_name,
            "emergency_contact_phone_number": instance.emergency_contact_phone_number,
            "primary_learning_support_category": instance.primary_learning_support_category,
            "assigned_learning_support_assistant_identifier": (
                instance.assigned_learning_support_assistant_identifier
            ),
            "regional_jurisdiction": instance.regional_jurisdiction,
            "dcyn_has_prior_formal_diagnosis": instance.dcyn_has_prior_formal_diagnosis,
            "dcyn_requires_one_on_one_support": instance.dcyn_requires_one_on_one_support,
            "dcyn_has_individualized_education_plan": (
                instance.dcyn_has_individualized_education_plan
            ),
            "dcyn_requires_non_verbal_communication_assistance": (
                instance.dcyn_requires_non_verbal_communication_assistance
            ),
            "dcyn_has_physical_mobility_assistance_needs": (
                instance.dcyn_has_physical_mobility_assistance_needs
            ),
            "dcyn_is_independently_toilet_trained": instance.dcyn_is_independently_toilet_trained,
            "dcyn_has_sensory_sensitivity_triggers": (
                instance.dcyn_has_sensory_sensitivity_triggers
            ),
            "dcyn_parental_data_processing_consent_granted": (
                instance.dcyn_parental_data_processing_consent_granted
            ),
            "dcyn_emergency_medical_action_plan_available": (
                instance.dcyn_emergency_medical_action_plan_available
            ),
            "dcyn_transportation_assistance_required": (
                instance.dcyn_transportation_assistance_required
            ),
            "ingestion_timestamp": instance.ingestion_timestamp.isoformat(),
            "schema_version": instance.schema_version,
            "data_payload_sha256_hash": instance.data_payload_sha256_hash,
        }

    def to_pubsub_message(self, instance: StudentOnboardingProfile) -> bytes:
        """Encodes validated record as UTF-8 JSON for streaming to Google Cloud Pub/Sub."""
        row_dict = self.to_bigquery_row(instance)
        return json.dumps(row_dict, sort_keys=True).encode("utf-8")

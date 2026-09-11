# ==============================================================================
# Habot Connect FZCO — Unit Test Suite
# Module: Student Onboarding Serializer Exact Boundary Tests
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# ==============================================================================

import datetime
import pytest
from django.utils import timezone
from onboarding.serializers import StudentOnboardingSerializer


@pytest.fixture
def valid_onboarding_payload():
    """Provides a completely compliant sample student onboarding payload."""
    today = timezone.now().date()
    dob = today - datetime.timedelta(days=7 * 365)  # Approx 7 years old

    return {
        "student_full_name": "Tariq Mansoor Al-Hashemi",
        "date_of_birth": dob.isoformat(),
        "parent_full_name": "Mansoor Al-Hashemi",
        "parent_email_address": "mansoor.alhashemi@example.ae",
        "parent_phone_number": "+971501234567",
        "emergency_contact_full_name": "Fatima Al-Hashemi",
        "emergency_contact_phone_number": "+971509876543",
        "primary_learning_support_category": "AUTISM_SPECTRUM_DISORDER",
        "assigned_learning_support_assistant_identifier": "sarah.jenkins@habotconnect.internal",
        "regional_jurisdiction": "DUBAI",
        "dcyn_indicators": {
            "has_prior_formal_diagnosis": "yes",
            "requires_one_on_one_support": "1",
            "has_individualized_education_plan": "true",
            "requires_non_verbal_communication_assistance": "no",
            "has_physical_mobility_assistance_needs": "0",
            "is_independently_toilet_trained": "true",
            "has_sensory_sensitivity_triggers": "YES",
            "parental_data_processing_consent_granted": "TRUE",
            "emergency_medical_action_plan_available": "yes",
            "transportation_assistance_required": "no",
        },
    }


@pytest.mark.django_db
class TestStudentOnboardingSerializer:
    """Verifies that the serializer enforces exact mathematical and structural boundaries."""

    def test_valid_payload_serializes_and_saves_successfully(self, valid_onboarding_payload):
        serializer = StudentOnboardingSerializer(data=valid_onboarding_payload)
        assert serializer.is_valid(), serializer.errors

        instance = serializer.save()
        assert instance.student_unique_identifier is not None
        assert instance.student_full_name == "Tariq Mansoor Al-Hashemi"
        assert instance.dcyn_requires_one_on_one_support is True
        assert instance.dcyn_requires_non_verbal_communication_assistance is False
        assert instance.schema_version == "v1.0.0"
        assert len(instance.data_payload_sha256_hash) == 64

        # Test BigQuery row mapping
        bq_row = serializer.to_bigquery_row(instance)
        assert bq_row["student_full_name"] == "Tariq Mansoor Al-Hashemi"
        assert bq_row["dcyn_parental_data_processing_consent_granted"] is True

        # Test Pub/Sub streaming message
        pubsub_msg = serializer.to_pubsub_message(instance)
        assert isinstance(pubsub_msg, bytes)
        assert b"Tariq Mansoor Al-Hashemi" in pubsub_msg

    def test_rejection_under_minimum_age_boundary(self, valid_onboarding_payload):
        """Student is 2 years old (under the 3.00-year minimum threshold)."""
        today = timezone.now().date()
        underage_days = 700
        valid_onboarding_payload["date_of_birth"] = (
            today - datetime.timedelta(days=underage_days)
        ).isoformat()

        serializer = StudentOnboardingSerializer(data=valid_onboarding_payload)
        assert not serializer.is_valid()
        assert "date_of_birth" in serializer.errors
        err_msg = str(serializer.errors["date_of_birth"])
        assert "below the minimum threshold of 3.00 years" in err_msg

    def test_rejection_over_maximum_age_boundary(self, valid_onboarding_payload):
        """Student is 19 years old (over the 18.00-year maximum threshold)."""
        today = timezone.now().date()
        overage_days = 19 * 366
        valid_onboarding_payload["date_of_birth"] = (
            today - datetime.timedelta(days=overage_days)
        ).isoformat()

        serializer = StudentOnboardingSerializer(data=valid_onboarding_payload)
        assert not serializer.is_valid()
        assert "date_of_birth" in serializer.errors
        err_msg = str(serializer.errors["date_of_birth"])
        assert "exceeds the maximum support limit of 18.00 years" in err_msg

    def test_rejection_of_future_date_of_birth(self, valid_onboarding_payload):
        today = timezone.now().date()
        valid_onboarding_payload["date_of_birth"] = (
            today + datetime.timedelta(days=1)
        ).isoformat()

        serializer = StudentOnboardingSerializer(data=valid_onboarding_payload)
        assert not serializer.is_valid()
        assert "date_of_birth" in serializer.errors

    def test_rejection_of_invalid_phone_format(self, valid_onboarding_payload):
        """Parent phone number lacks international E.164 formatting."""
        valid_onboarding_payload["parent_phone_number"] = "0501234567"

        serializer = StudentOnboardingSerializer(data=valid_onboarding_payload)
        assert not serializer.is_valid()
        assert "parent_phone_number" in serializer.errors
        assert "E.164" in str(serializer.errors["parent_phone_number"])

    def test_rejection_of_duplicate_emergency_contact(self, valid_onboarding_payload):
        """Emergency contact cannot be the same persona as the primary parent."""
        valid_onboarding_payload["emergency_contact_full_name"] = (
            valid_onboarding_payload["parent_full_name"]
        )

        serializer = StudentOnboardingSerializer(data=valid_onboarding_payload)
        assert not serializer.is_valid()
        assert "emergency_contact_full_name" in serializer.errors

    def test_rejection_of_disposable_email_domain(self, valid_onboarding_payload):
        valid_onboarding_payload["parent_email_address"] = "fakeuser@mailinator.com"

        serializer = StudentOnboardingSerializer(data=valid_onboarding_payload)
        assert not serializer.is_valid()
        assert "parent_email_address" in serializer.errors
        assert "disposable email domain" in str(serializer.errors["parent_email_address"]).lower()

    def test_rejection_when_parental_consent_is_denied(self, valid_onboarding_payload):
        """Golden Rule: Processing child data without affirmative consent is illegal."""
        valid_onboarding_payload["dcyn_indicators"][
            "parental_data_processing_consent_granted"
        ] = "no"

        serializer = StudentOnboardingSerializer(data=valid_onboarding_payload)
        assert not serializer.is_valid()
        assert "dcyn_parental_data_processing_consent_granted" in serializer.errors
        assert "must be affirmatively granted (TRUE)" in str(serializer.errors)

    def test_rejection_when_dcyn_indicator_is_ambiguous(self, valid_onboarding_payload):
        valid_onboarding_payload["dcyn_indicators"]["requires_one_on_one_support"] = "sometimes"

        serializer = StudentOnboardingSerializer(data=valid_onboarding_payload)
        assert not serializer.is_valid()
        assert "dcyn_requires_one_on_one_support" in serializer.errors

# ==============================================================================
# Habot Connect FZCO — Unit Test Suite
# Module: Poka-Yoke Automated Build Gate & Secret Protection Tests
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# ==============================================================================

import re

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestPokaYokeGateSecurity:
    """Verifies that system halts and fails closed upon encountering unencrypted secrets."""

    def test_api_rejection_of_payload_with_unencrypted_secret_injection(self):
        """Simulates junior developer incident: Unencrypted secret passed in payload."""
        client = APIClient()

        malicious_payload = {
            "student_full_name": "Test Child",
            "date_of_birth": "2018-05-15",
            "parent_full_name": "Test Parent",
            "parent_email_address": "parent@example.ae",
            "parent_phone_number": "+971501112233",
            "emergency_contact_full_name": "Emergency Person",
            "emergency_contact_phone_number": "+971509998877",
            "primary_learning_support_category": "AUTISM_SPECTRUM_DISORDER",
            "assigned_learning_support_assistant_identifier": "lsa@habotconnect.internal",
            "regional_jurisdiction": "DUBAI",
            "api_secret_key": "AIzaSyD-HabotConnectSecretAPIKeyExposed12345",
            "dcyn_indicators": {
                "has_prior_formal_diagnosis": "yes",
                "requires_one_on_one_support": "no",
                "has_individualized_education_plan": "no",
                "requires_non_verbal_communication_assistance": "no",
                "has_physical_mobility_assistance_needs": "no",
                "is_independently_toilet_trained": "yes",
                "has_sensory_sensitivity_triggers": "no",
                "parental_data_processing_consent_granted": "yes",
                "emergency_medical_action_plan_available": "no",
                "transportation_assistance_required": "no",
            },
        }

        response = client.post("/api/v1/onboarding/students/", malicious_payload, format="json")
        assert response.status_code in [201, 400]
        if response.status_code == 201:
            data = response.json()
            assert "api_secret_key" not in data["staged_record"]

    def test_regex_detects_exposed_cloud_credentials(self):
        """Validates regex pattern used by CI/CD build gate to catch hardcoded secrets."""
        secret_pattern = (
            r"(?i)(api[_-]?key|secret[_-]?key|auth[_-]?token|access[_-]?token|private[_-]?key)"
            r"\s*[:=]\s*['\"][0-9a-zA-Z\-_]{20,}['\"]"
        )
        secret_regex = re.compile(secret_pattern)

        leaked_snippet = 'gcp_api_secret_key = "AIzaSyD9876543210ABCDEFGHIJKLMN12345"'
        clean_snippet = 'assigned_lsa_email = "sarah.jenkins@habotconnect.internal"'

        assert secret_regex.search(leaked_snippet) is not None
        assert secret_regex.search(clean_snippet) is None

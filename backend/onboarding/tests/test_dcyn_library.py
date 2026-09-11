# ==============================================================================
# Habot Connect FZCO — Unit Test Suite
# Module: DCYN Binary Logic Library Validation Tests
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# ==============================================================================

import pytest
from onboarding.dcyn_library import (
    DCYN_STUDENT_QUESTION_CATALOG,
    DCYNTransformer,
    DCYNValidationError,
)


class TestDCYNTransformer:
    """Rigorous verification of deterministic boolean transformations."""

    @pytest.mark.parametrize(
        "truthy_input",
        [
            True,
            1,
            "true",
            "True",
            "TRUE",
            "yes",
            "YES",
            "Yes",
            "y",
            "Y",
            "1",
            "  yes  ",
        ],
    )
    def test_deterministic_affirmative_resolution(self, truthy_input):
        result = DCYNTransformer.to_boolean("test_field", truthy_input)
        assert result is True
        assert isinstance(result, bool)

    @pytest.mark.parametrize(
        "falsy_input",
        [
            False,
            0,
            "false",
            "False",
            "FALSE",
            "no",
            "NO",
            "No",
            "n",
            "N",
            "0",
            "  no  ",
        ],
    )
    def test_deterministic_negative_resolution(self, falsy_input):
        result = DCYNTransformer.to_boolean("test_field", falsy_input)
        assert result is False
        assert isinstance(result, bool)

    @pytest.mark.parametrize(
        "ambiguous_input",
        [
            "maybe",
            "partially",
            "sometimes",
            "unknown",
            "undecided",
            "n/a",
            "na",
            "null",
            "none",
            "pending",
            "unclear",
            "inapplicable",
        ],
    )
    def test_strict_rejection_of_ambiguous_values(self, ambiguous_input):
        """Golden Rule: Disallow any human subjective interpretation."""
        with pytest.raises(DCYNValidationError) as exc_info:
            DCYNTransformer.to_boolean("has_prior_formal_diagnosis", ambiguous_input)
        assert "violates HabotConnect zero-judgment rule" in str(exc_info.value)

    @pytest.mark.parametrize(
        "invalid_type_or_value",
        [
            None,
            "",
            "   ",
            2,
            -1,
            99,
            3.14,
            ["yes"],
            {"answer": "yes"},
            "invalid_text",
        ],
    )
    def test_strict_rejection_of_unsupported_inputs(self, invalid_type_or_value):
        with pytest.raises(DCYNValidationError):
            DCYNTransformer.to_boolean("test_field", invalid_type_or_value)

    def test_dcyn_catalog_completeness(self):
        """Assert exactly 10 standardized clinical and operational questions exist."""
        assert len(DCYN_STUDENT_QUESTION_CATALOG) == 10
        expected_keys = {
            "has_prior_formal_diagnosis",
            "requires_one_on_one_support",
            "has_individualized_education_plan",
            "requires_non_verbal_communication_assistance",
            "has_physical_mobility_assistance_needs",
            "is_independently_toilet_trained",
            "has_sensory_sensitivity_triggers",
            "parental_data_processing_consent_granted",
            "emergency_medical_action_plan_available",
            "transportation_assistance_required",
        }
        assert set(DCYN_STUDENT_QUESTION_CATALOG.keys()) == expected_keys

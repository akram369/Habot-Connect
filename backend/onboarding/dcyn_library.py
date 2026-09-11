# ==============================================================================
# Habot Connect FZCO — Deterministic Clean Yes/No (DCYN) Binary Logic Library
# Module: DCYN Automated Mistake-Proofing Validation Library
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# Date: September 2026
# ==============================================================================

from typing import Any, Dict, Final, FrozenSet


class DCYNValidationError(ValueError):
    """
    Exception raised when an incoming field cannot be deterministically mapped
    to a binary Yes/No (True/False) value without ambiguity.
    """

    def __init__(self, field_name: str, raw_value: Any, reason: str):
        self.field_name = field_name
        self.raw_value = raw_value
        self.reason = reason
        super().__init__(
            f"DCYN Validation Failure on field '{field_name}': Received value "
            f"{repr(raw_value)} which violates deterministic binary logic. Reason: {reason}"
        )


class DCYNTransformer:
    """
    Poka-Yoke (Mistake-Proofing) Engine for Deconstructing and Normalizing
    Incoming Student Evaluation Data into Strict Binary (Yes/No) Truth Values.

    Eliminates all human discretion, assumptions, and fuzzy states.
    """

    TRUTHY_STRING_LITERALS: Final[FrozenSet[str]] = frozenset({"true", "yes", "y", "1"})

    FALSY_STRING_LITERALS: Final[FrozenSet[str]] = frozenset({"false", "no", "n", "0"})

    EXPLICITLY_PROHIBITED_AMBIGUOUS_VALUES: Final[FrozenSet[str]] = frozenset(
        {
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
        }
    )

    @classmethod
    def _parse_string(cls, field_name: str, raw_value: str) -> bool:
        cleaned_value = raw_value.strip().lower()
        if not cleaned_value:
            raise DCYNValidationError(
                field_name=field_name,
                raw_value=raw_value,
                reason="Empty string cannot be evaluated to a binary Yes/No state.",
            )
        if cleaned_value in cls.EXPLICITLY_PROHIBITED_AMBIGUOUS_VALUES:
            raise DCYNValidationError(
                field_name=field_name,
                raw_value=raw_value,
                reason=(
                    f"Ambiguous value '{raw_value}' violates HabotConnect zero-judgment rule. "
                    "Questions must be answered with unequivocal certainty."
                ),
            )
        if cleaned_value in cls.TRUTHY_STRING_LITERALS:
            return True
        if cleaned_value in cls.FALSY_STRING_LITERALS:
            return False
        raise DCYNValidationError(
            field_name=field_name,
            raw_value=raw_value,
            reason=f"Unrecognized textual representation '{raw_value}'.",
        )

    @classmethod
    def to_boolean(cls, field_name: str, raw_value: Any) -> bool:
        """Transforms and validates raw input into a pure Python boolean (True/False)."""
        if raw_value is None:
            raise DCYNValidationError(
                field_name=field_name,
                raw_value=raw_value,
                reason="Null and missing values are strictly forbidden in DCYN schema.",
            )
        if isinstance(raw_value, bool):
            return raw_value
        if isinstance(raw_value, int):
            if raw_value == 1:
                return True
            if raw_value == 0:
                return False
            raise DCYNValidationError(
                field_name=field_name,
                raw_value=raw_value,
                reason=f"Integer value {raw_value} is not a valid binary state (0 or 1).",
            )
        if isinstance(raw_value, str):
            return cls._parse_string(field_name, raw_value)

        raise DCYNValidationError(
            field_name=field_name,
            raw_value=raw_value,
            reason=f"Unsupported data type '{type(raw_value).__name__}' passed to DCYN.",
        )


# ==============================================================================
# Standard Catalog of DCYN Student Assessment Indicators
# ==============================================================================
DCYN_STUDENT_QUESTION_CATALOG: Final[Dict[str, Dict[str, str]]] = {
    "has_prior_formal_diagnosis": {
        "full_question_name": "Has Formal Medical or Psychological Diagnosis",
        "description": "Indicates whether student possesses a formal clinical evaluation report.",
        "category": "Clinical Assessment",
    },
    "requires_one_on_one_support": {
        "full_question_name": "Requires Dedicated One-on-One Assistant",
        "description": "Specifies requirement for 100% individual LSA time.",
        "category": "Resource Allocation",
    },
    "has_individualized_education_plan": {
        "full_question_name": "Has Active Individualized Education Plan",
        "description": "Verifies whether an official IEP document exists on file.",
        "category": "Academic Support",
    },
    "requires_non_verbal_communication_assistance": {
        "full_question_name": "Requires Non-Verbal Communication Assistance",
        "description": "Specifies requirement for Picture Exchange or speech generation tools.",
        "category": "Communication Needs",
    },
    "has_physical_mobility_assistance_needs": {
        "full_question_name": "Has Physical Mobility Assistance Needs",
        "description": "Specifies whether student requires wheelchair or physical guidance.",
        "category": "Physical Support",
    },
    "is_independently_toilet_trained": {
        "full_question_name": "Is Independently Restroom and Hygiene Trained",
        "description": "Evaluates whether personal care assistance is required during school.",
        "category": "Self Care Independence",
    },
    "has_sensory_sensitivity_triggers": {
        "full_question_name": "Has Extreme Sensory Sensitivity Triggers",
        "description": "Flags severe acoustic, tactile, or visual hypersensitivities.",
        "category": "Environmental Adaptation",
    },
    "parental_data_processing_consent_granted": {
        "full_question_name": "Parental Data Processing Legal Consent Granted",
        "description": "Mandatory legal consent for minor student data handling under UAE Law.",
        "category": "Legal Compliance",
    },
    "emergency_medical_action_plan_available": {
        "full_question_name": "Emergency Medical Action Plan Available",
        "description": "Flags presence of critical pediatric allergy or medical protocols.",
        "category": "Health & Safety",
    },
    "transportation_assistance_required": {
        "full_question_name": "Specialized Transportation Assistance Required",
        "description": "Flags requirement for adapted transit vehicle accommodations.",
        "category": "Logistics & Transport",
    },
}

# ==============================================================================
# Habot Connect FZCO — API Views
# Module: Student Onboarding Ingestion & Streaming Sink API
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# Date: September 2026
# ==============================================================================

import logging

from onboarding.serializers import StudentOnboardingSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger("habotconnect.onboarding")


class StudentOnboardingIngestionView(APIView):
    """
    Ingestion Endpoint for Student Onboarding Submissions.
    Executes zero-judgment validation, DCYN binary deconstruction,
    persists record, and simulates streaming to Google Cloud Pub/Sub & BigQuery D1.
    """

    def post(self, request, *args, **kwargs):
        serializer = StudentOnboardingSerializer(data=request.data)

        if not serializer.is_valid():
            logger.warning(
                "Poka-Yoke Ingestion Gate Blocked Non-Compliant Payload: %s",
                serializer.errors,
            )
            return Response(
                {
                    "status": "FAIL_CLOSED_VALIDATION_ERROR",
                    "error_code": "HABOT_SCHEMA_VALIDATION_FAILURE",
                    "details": serializer.errors,
                    "remediation": (
                        "Review exact boundary rules in the HabotConnect "
                        "DCYN Data Schema Mapping specification."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile_instance = serializer.save()
        bigquery_payload = serializer.to_bigquery_row(profile_instance)

        logger.info(
            "Successfully Ingested Student Profile: %s (Audit Hash: %s)",
            profile_instance.student_unique_identifier,
            profile_instance.data_payload_sha256_hash,
        )

        stream_target = (
            "projects/habotconnect-staging-2026/datasets/"
            "habotconnect_d1_staged_enforced/tables/student_onboarding_staged"
        )

        return Response(
            {
                "status": "SUCCESSFULLY_INGESTED",
                "student_unique_identifier": str(profile_instance.student_unique_identifier),
                "schema_version": profile_instance.schema_version,
                "ingestion_timestamp": profile_instance.ingestion_timestamp.isoformat(),
                "data_payload_sha256_hash": profile_instance.data_payload_sha256_hash,
                "streaming_sink_target": stream_target,
                "staged_record": bigquery_payload,
            },
            status=status.HTTP_201_CREATED,
        )


class HealthCheckView(APIView):
    """Simple health check endpoint for container probes."""

    def get(self, request):
        return Response(
            {
                "service": "habotconnect-onboarding-service",
                "status": "HEALTHY",
                "poka_yoke_build_gate": "ENFORCED",
            }
        )

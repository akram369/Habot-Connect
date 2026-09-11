# ==============================================================================
# Habot Connect FZCO — Onboarding Application URLs
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# ==============================================================================

from django.urls import path
from onboarding.views import HealthCheckView, StudentOnboardingIngestionView

urlpatterns = [
    path("students/", StudentOnboardingIngestionView.as_view(), name="student-onboarding-ingest"),
    path("health/", HealthCheckView.as_view(), name="health-check"),
]

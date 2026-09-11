# ==============================================================================
# Habot Connect FZCO — Core Routing
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# ==============================================================================

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/onboarding/", include("onboarding.urls")),
]

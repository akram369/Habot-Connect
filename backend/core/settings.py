# ==============================================================================
# Habot Connect FZCO — Django Application Settings
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# Profile: https://www.linkedin.com/in/shaik-akram08/ | https://github.com/akram369
# ==============================================================================

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Poka-Yoke Fail-Closed Secret Key Loading
# Never allow unencrypted raw secrets in repository code
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    if (
        any(arg in sys.argv for arg in ("test", "makemigrations", "migrate", "check"))
        or "pytest" in sys.modules
        or os.getenv("ENVIRONMENT") in ("testing", "development")
    ):
        SECRET_KEY = "temporary-ci-testing-key-never-used-in-production"
    else:
        raise RuntimeError(
            "CRITICAL SECURITY VIOLATION: DJANGO_SECRET_KEY environment variable is missing. "
            "Poka-Yoke Fail-Closed Rule enforced: Application startup halted."
        )

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,staging.habotconnect.internal,habot.io"
).split(",")

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party extensions
    "rest_framework",
    # HabotConnect Domain Apps
    "onboarding.apps.OnboardingConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "staging_habotconnect.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dubai"  # Compliant with HabotConnect UAE Operations
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework Strict Configuration
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # Ingestion is token-authenticated in custom view
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "UNAUTHENTICATED_USER": None,
}

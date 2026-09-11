# ==============================================================================
# Habot Connect FZCO — WSGI Configuration
# Candidate: Shaik Akram | +91 6302806015 | akramshaik1512@gmail.com
# ==============================================================================

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
application = get_wsgi_application()

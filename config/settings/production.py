import os

import dj_database_url

from .base import *

DEBUG = False
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
DATABASES['default'] = dj_database_url.config(
    default=os.getenv('DATABASE_URL', f"sqlite:///{BASE_DIR / os.getenv('DJANGO_DB_NAME', 'db.sqlite3')}"),
    conn_max_age=600,
)
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False

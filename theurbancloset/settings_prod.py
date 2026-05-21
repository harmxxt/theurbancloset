"""
TheUrbanCloset Production Settings
Used when deploying to Render or any production server.
Usage: set DJANGO_SETTINGS_MODULE=theurbancloset.settings_prod

This file imports base settings and overrides only what needs to change.
"""

from .settings import *
import os

# ---- Security ----
DEBUG = False

# Add your Render URL here, e.g. 'theurbancloset.onrender.com'
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# HTTPS security headers
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# ---- Database (use PostgreSQL on production if needed) ----
# Uncomment and fill in if using PostgreSQL on Render:
# import dj_database_url
# DATABASES = {
#     'default': dj_database_url.config(default=config('DATABASE_URL'))
# }

# ---- Static files ----
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---- Logging ----
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'orders': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'invoices': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    },
}

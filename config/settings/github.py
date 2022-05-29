import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .base import *  # noqa
from .base import env


###############################################################################
# DJANGO DEV PANEL RECOMMENDATIONS AND OTHER SECURITY
###############################################################################

DEBUG = False


###############################################################################
# DATABASE CONFIG
###############################################################################

DATABASES = {
    "default": {
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.str("POSTGRES_PORT", None),
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": env.int("CONN_MAX_AGE", default=60)
    },
}


###############################################################################
# STORAGES
###############################################################################

INSTALLED_APPS += ["storages"]
GS_BUCKET_NAME = env.str("DJANGO_GCP_STORAGE_BUCKET_NAME")
GS_DEFAULT_ACL = "project-private"


###############################################################################
# DJANGO COMPRESSOR
###############################################################################

COMPRESS_ENABLED = True
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_URL
COMPRESS_URL = STATIC_URL  # noqa F405
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True  # Offline compression is required when using Whitenoise
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_FILTERS
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}


###############################################################################
# STATIC ASSETS AND MEDIA FILES
###############################################################################

DEFAULT_FILE_STORAGE = "utils.storages.MediaRootGoogleCloudStorage"
MEDIA_URL = "https://storage.googleapis.com/%s/media/" % GS_BUCKET_NAME
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

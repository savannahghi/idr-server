"""
Django settings for idr_server project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

import environs

###############################################################################
# READ ENVIRONMENT
###############################################################################
env = environs.Env()

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=[
        ".fahariyajamii.org",
        "idr.fahariyajamii.org",
        "icdr.fahariyajamii.org",
    ],
)
DEBUG = env.bool("DJANGO_DEBUG", False)
DJANGO_LOG_LEVEL = env.str("DJANGO_LOG_LEVEL", default="DEBUG")
SECRET_KEY = env.str("DJANGO_SECRET_KEY", "django-insecure-xlb*ys8xwb04c&=y_z")


###############################################################################
# FILE SYSTEM AND MISC
###############################################################################
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


###############################################################################
# DJANGO DEV PANEL RECOMMENDATIONS AND OTHER SECURITY
###############################################################################

CSRF_USE_SESSIONS = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"


###############################################################################
# INSTALLED APPS
###############################################################################

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "compressor",
    "crispy_forms",
    "django_extensions",
    "django_filters",
    "knox",
    "rest_framework",
    "rest_framework.authtoken",
]

LOCAL_APPS = [
    "apps.app_auth.apps.AppAuthConfig",
    "apps.common.apps.CommonConfig",
    "apps.core.apps.CoreConfig",
    "apps.dashboards.apps.DashboardsConfig",
    "apps.frontend.apps.FrontendConfig",
    "apps.misc.apps.MiscConfig",
    "apps.sql_data.apps.SqlDataConfig",
    "apps.users.apps.UsersConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


###############################################################################
# MIDDLEWARE
###############################################################################

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


###############################################################################
# CORE DJANGO CONFIG
###############################################################################

APPEND_SLASH = True
ASGI_APPLICATION = "config.asgi.application"
BASE_URL = "http://localhost:8000"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
INTERNAL_IPS = ["127.0.0.1"]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"


###############################################################################
# TEMPLATES
###############################################################################

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["assets/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.contrib.messages.context_processors.messages",
                "apps.frontend.context_processors.dashboards",
            ],
        },
    },
]


###############################################################################
# DRF
###############################################################################

REST_FRAMEWORK = {
    "DEFAULT_MODEL_SERIALIZER_CLASS": (
        "rest_framework.serializers.ModelSerializer",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.AdminRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": 100,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "knox.auth.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.DjangoModelPermissions",
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework.metadata.SimpleMetadata",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"user": "1000/second", "anon": "1000/minute"},
    "DATETIME_FORMAT": "iso-8601",
    "DATE_FORMAT": "iso-8601",
    "TIME_FORMAT": "iso-8601",
}
CORS_URLS_REGEX = r"^/api/.*$"


###############################################################################
# TRANSLATIONS AND LOCALES
###############################################################################
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
# USE_L10N = True
USE_TZ = True


###############################################################################
# STATIC ASSETS AND MEDIA FILES
###############################################################################

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "assets" / "static"]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

WHITENOISE_MANIFEST_STRICT = False


###############################################################################
# AUTH AND PASSWORDS
###############################################################################

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"  # noqa
    },
]
AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
LOGIN_REDIRECT_URL = "home"
LOGIN_URL = "account_login"


###############################################################################
# DJANGO ALL AUTH
###############################################################################

ACCOUNT_ALLOW_REGISTRATION = env.bool(
    "DJANGO_ACCOUNT_ALLOW_REGISTRATION", True
)
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_ADAPTER = "apps.users.adapters.AccountAdapter"
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_SESSION_REMEMBER = None  # ask the user 'Remember me'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
SOCIALACCOUNT_ADAPTER = "apps.users.adapters.SocialAccountAdapter"
SOCIALACCOUNT_AUTO_SIGNUP = True


###############################################################################
# LOGGING
###############################################################################

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            )
        }
    },
    "handlers": {
        "console": {
            "level": DJANGO_LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}


###############################################################################
# OTHER
###############################################################################

ADMIN_URL = "admin/"


###############################################################################
# PROJECT SPECIFIC
###############################################################################

BASE_EXTRACTS_UPLOAD_DIR_NAME = "extracts"
"""
This is the name of the root dir where all extracts uploads are stored.

This will typically be: MEDIA_ROOT/BASE_EXTRACTS_UPLOADS_DIR_NAME
"""

SQL_EXTRACTS_UPLOAD_DIR_NAME = "sql_extracts"
"""
This is the name of the root dir where all sql extracts uploads are stored.

This will typically be:
MEDIA_ROOT/BASE_EXTRACTS_UPLOADS_DIR_NAME/SQL_EXTRACTS_UPLOAD_DIR_NAME
"""

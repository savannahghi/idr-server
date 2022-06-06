from .base import *  # noqa
from .base import env

###############################################################################
# DATABASE CONFIG
###############################################################################

DATABASES = {
    "default": {
        "NAME": env.str("TEST_POSTGRES_DB"),
        "USER": env.str("TEST_POSTGRES_USER"),
        "PASSWORD": env.str("TEST_POSTGRES_PASSWORD"),
        "HOST": env.str("TEST_POSTGRES_HOST"),
        "PORT": env.str("TEST_POSTGRES_PORT", None),
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "ATOMIC_REQUESTS": True,
        "TEST": {
            "NAME": env.str("TEST_POSTGRES_DB"),
            "USER": env.str("TEST_POSTGRES_USER"),
            "PASSWORD": env.str("TEST_POSTGRES_PASSWORD"),
        },
    },
}


###############################################################################
# EMAIL
###############################################################################

# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


###############################################################################
# FAKER
###############################################################################

# https://faker.readthedocs.io/en/master/
FAKER = {"DEFAULT_LOCALE": "en_US"}


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
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_LEVEL", default="ERROR"),
        },
    },
}


###############################################################################
# TEMPLATES
###############################################################################

TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

from .base import *  # noqa
from .base import env


###############################################################################
# INSTALLED APPS
###############################################################################

INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS


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
    },
}

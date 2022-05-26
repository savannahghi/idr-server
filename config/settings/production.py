from .base import *  # noqa
from .base import env


###############################################################################
# LOAD ENVIRONMENT
###############################################################################
ENV_PATH = "/tmp/secrets/.env"
env.read_env(path=ENV_PATH, override=True)

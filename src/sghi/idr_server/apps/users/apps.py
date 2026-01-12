from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "sghi.idr_server.apps.users"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("Users")

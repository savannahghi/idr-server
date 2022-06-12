from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppAuthConfig(AppConfig):
    name = "apps.app_auth"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("Auth")

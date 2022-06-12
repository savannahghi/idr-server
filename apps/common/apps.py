from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommonConfig(AppConfig):
    name = "apps.common"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("Common")

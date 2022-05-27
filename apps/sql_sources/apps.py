from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SqlSourcesConfig(AppConfig):
    name = "apps.sql_sources"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("Sql Sources")

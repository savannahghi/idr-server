from django.contrib import admin

from apps.core.admin import AuditBaseModelAdmin

from .models import GenericSource


@admin.register(GenericSource)
class GenericSourceAdmin(AuditBaseModelAdmin):
    list_display = ("name", "description")

from django.contrib import admin

from apps.core.admin import AuditBaseModelAdmin

from .models import SimpleSqlMetadata, SourceVersion


@admin.register(SimpleSqlMetadata)
class SimpleSqlMetadata(AuditBaseModelAdmin):
    list_display = ("name", "version", "description")


@admin.register(SourceVersion)
class SourceVersionAdmin(AuditBaseModelAdmin):
    list_display = ("source", "source_version")

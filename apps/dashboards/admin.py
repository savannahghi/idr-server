from django.contrib import admin

from apps.core.admin import AuditBaseModelAdmin

from .models import Dashboard, Visualization


@admin.register(Dashboard)
class DashboardAdmin(AuditBaseModelAdmin):
    filter_horizontal = ("visualizations",)
    list_display = ("title", "description", "is_published")


@admin.register(Visualization)
class VisualizationAdmin(AuditBaseModelAdmin):
    list_display = ("title", "description", "is_published")

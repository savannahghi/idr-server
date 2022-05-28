from decimal import Decimal
from typing import Any, Mapping

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AuditBase, AuditBaseManager, BaseQuerySet


# =============================================================================
# CONSTANTS
# =============================================================================

_DEFAULT_VISUALIZATION_ATTRIBUTES: Mapping[str, Any] = {
    "allowFullScreen": "true",
    "frameboarder": 0
}


# =============================================================================
# HELPERS
# =============================================================================

def _default_visualization_attrs_factory() -> Mapping[str, Any]:
    return _DEFAULT_VISUALIZATION_ATTRIBUTES


# =============================================================================
# QUERY SETS
# =============================================================================

class DashboardQuerySet(BaseQuerySet):
    """The query set for the Dashboard models."""

    def published(self) -> "DashboardQuerySet":
        """Return a queryset containing published dashboards only."""
        return self.filter(is_published=True)


class VisualizationQuerySet(BaseQuerySet):
    """The Query set for the Visualization models."""

    def published(self) -> "Visualization":
        """Return a queryset containing published visualizations only."""
        return self.filter(is_published=True)


# =============================================================================
# MANAGERS
# =============================================================================

class DashboardManager(AuditBaseManager.from_queryset(DashboardQuerySet)):
    """Manager for the dashboard model."""
    use_in_migrations = True

    def get_queryset(self) -> DashboardQuerySet:
        return DashboardQuerySet(self.model, using=self._db)


class VisualizationManager(
    AuditBaseManager.from_queryset(VisualizationQuerySet)
):
    """Manager for the visualization model."""
    use_in_migrations = True

    def get_queryset(self) -> VisualizationQuerySet:
        return VisualizationQuerySet(self.model, using=self._db)


# =============================================================================
# MODELS
# =============================================================================

class Dashboard(AuditBase):
    """This represents a collection of related visualizations."""
    class DashboardLayouts(models.TextChoices):
        """The different layouts that are supported by dashboards."""
        FREE_LAYOUT = "free", _("Free Layout")
        NOT_SPECIFIED = "none", _("Not Specified")

    title = models.CharField(
        max_length=200,
        help_text=_("A descriptive title for this dashboard.")
    )
    description = models.TextField(blank=True, default="")
    layout = models.CharField(
        choices=DashboardLayouts.choices,
        default=DashboardLayouts.NOT_SPECIFIED.value,
        max_length=15
    )
    weight = models.SmallIntegerField(
        blank=True,
        default=0,
        verbose_name=_("Weight/Precedence"),
        help_text=_(
            "This indicates the importance of this dashboard. Dashboards with "
            "higher weights/precedence should generally be displayed before "
            "those with lower weights."
        )
    )
    visualizations = models.ManyToManyField("Visualization")
    is_published = models.BooleanField(
        default=False,
        help_text=_(
            "This flag indicates whether a dashboard and it's visualizations "
            "are ready for consumption by the stakeholders/users."
        )
    )

    # Override the default manager
    objects = DashboardManager()

    def __str__(self) -> str:
        return self.title


class Visualization(AuditBase):
    """Represents a chart/reports and other reporting items within a dashboard.

    The visualizations are embedded inside an iframe.
    """
    title = models.CharField(
        max_length=200,
        help_text=_("A descriptive title for this visualization.")
    )
    description = models.TextField(blank=True, default="")
    source = models.URLField(
        max_length=255,
        verbose_name=_("Visualization source"),
        help_text=_(
            "The url to the source of this visualization. E.g A url to a "
            "Power Bi dashboard."
        )
    )
    width = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("400.00"),
        help_text=_(
            "The width that the visualization should have in pixels once "
            "it's rendered."
        )
    )
    height = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("300.00"),
        help_text=_(
            "The height that the visualization should have in pixels once "
            "it's rendered."
        )
    )
    weight = models.SmallIntegerField(
        blank=True,
        default=0,
        verbose_name=_("Weight/Precedence"),
        help_text=_(
            "This indicates the importance of this visualization within a "
            "dashboard. Visualizations with higher weights/precedence should "
            "generally be displayed before those with lower weights but "
            "dashboards renders can choose to ignore these values and layout "
            "the visualizations however they see fit."
        )
    )
    metadata = models.JSONField(
        blank=True,
        default=_default_visualization_attrs_factory,
        verbose_name=_(
            "Metadata and attributes to append to the rendered visualizations."
            " These attributes are added as html element attributes to the "
            "rendered iframe (Should be a dict)."
        )
    )
    is_published = models.BooleanField(
        default=False,
        help_text=_(
            "This flag indicates whether a visualization is ready for "
            "consumption by the stakeholders/users."
        )
    )

    # Override the default manager
    objects = VisualizationManager()

    def __str__(self) -> str:
        return self.title

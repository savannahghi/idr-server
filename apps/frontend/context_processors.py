from typing import Any, Mapping

from django.http.request import HttpRequest

from apps.dashboards.models import Dashboard, DashboardQuerySet


def dashboards(request: HttpRequest) -> Mapping[str, Any]:
    """Add a dashboards queryset to each RequestContext.

    Note: Only admin users will be able to see unpublished dashboards.
    """
    dashboards_queryset: DashboardQuerySet
    if request.user.is_staff:
        dashboards_queryset = Dashboard.objects.order_by("-weight").all()
    else:
        dashboards_queryset = Dashboard.objects.published().order_by("-weight")
    return {"dashboards": dashboards_queryset}

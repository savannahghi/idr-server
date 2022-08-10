from apps.core.apiviews import AuditBaseViewSet

from .models import Dashboard, Visualization
from .serializers import DashboardSerializer, VisualizationSerializer


class DashboardViewSet(AuditBaseViewSet):
    """Dashboards API."""

    queryset = Dashboard.objects.published()
    serializer_class = DashboardSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Dashboard.objects.all()
        return super().get_queryset()


class VisualizationViewSet(AuditBaseViewSet):
    """Visualizations API."""

    queryset = Visualization.objects.published()
    serializer_class = VisualizationSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Visualization.objects.all()
        return super().get_queryset()

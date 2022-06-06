from apps.core.serializers import AuditBaseSerializer

from .models import Dashboard, Visualization


class VisualizationSerializer(AuditBaseSerializer):
    class Meta:
        model = Visualization
        fields = "__all__"


class DashboardSerializer(AuditBaseSerializer):
    visualizations = VisualizationSerializer(many=True, read_only=True)

    class Meta:
        model = Dashboard
        fields = "__all__"

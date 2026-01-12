from sghi.idr_server.apps.core.serializers import AuditBaseSerializer

from .models import GenericSource


class GenericSourceSerializer(AuditBaseSerializer):
    class Meta:
        model = GenericSource
        fields = "__all__"

from apps.core.apiviews import AuditBaseViewSet

from .models import GenericSource
from .serializers import GenericSourceSerializer


class GenericSourceViewSet(AuditBaseViewSet):
    """Generic Source API."""

    queryset = GenericSource.objects.all()
    serializer_class = GenericSourceSerializer

from apps.core.apiviews import AuditBaseViewSet

from .models import SimpleSqlMetadata, SourceVersion
from .serializers import SimpleSqlMetadataSerializer, SourceVersionSerializer


class SimpleMetadataViewSet(AuditBaseViewSet):
    """Simple Metadata API."""
    queryset = SimpleSqlMetadata.objects.all()
    serializer_class = SimpleSqlMetadataSerializer


class SourceVersionViewSet(AuditBaseViewSet):
    """Source Version API."""
    queryset = SourceVersion.objects.all()
    serializer_class = SourceVersionSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


from .models import GenericSource
from .serializers import GenericSourceSerializer


class BaseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated,]
    
    """
    This is the base `ViewSet` from which all other view sets are derived from.
    """
    ...


class AuditBaseViewSet(BaseViewSet):
    """
    This is the base `ViewSet` for all `AuditBase` models in this project.
    """
    ...


class GenericSourceViewSet(AuditBaseViewSet):
    """Generic Source API."""
    queryset = GenericSource.objects.all()
    serializer_class = GenericSourceSerializer

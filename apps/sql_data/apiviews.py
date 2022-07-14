from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.views import Request, Response
from rest_framework.viewsets import GenericViewSet
from apps.core.apiviews import AuditBaseViewSet

from .models import (
    DataSourceVersion,
    SQLDatabaseSource,
    SQLExtractMetadata,
    SQLUploadChunk,
    SQLUploadMetadata
)
from .serializers import (
    DataSourceVersionSerializer,
    NewSQLUploadChunkSerializer,
    SQLDatabaseSerializer,
    SQLExtractMetadataSerializer,
    SQLUploadChunkSerializer,
    SQLUploadMetadataSerializer
)


class DataSourceVersionViewSet(AuditBaseViewSet):
    """Data Source Version API."""
    queryset = DataSourceVersion.objects.all()
    serializer_class = DataSourceVersionSerializer
    filterset_fields = ['id', 'data_source', 'data_source_version']


class SQLDatabaseViewSet(AuditBaseViewSet):
    """SQL Database Sources API."""
    queryset = SQLDatabaseSource.objects.all()
    serializer_class = SQLDatabaseSerializer
    filterset_fields = ['id', 'name', 'database_name', 'database_vendor']


class SQLExtractMetadataViewSet(AuditBaseViewSet):
    """SQL Extract Metadata API."""
    queryset = SQLExtractMetadata.objects.prefetch_related(
        "applicable_source_versions", "data_source"
    ).all()
    serializer_class = SQLExtractMetadataSerializer
    filterset_fields = ['id', 'name', 'data_source__database_name', 'version', 'preferred_uploads_name']


class SQLUploadChunkViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """SQL Upload Chunk API."""
    queryset = SQLUploadChunk.objects.all()
    serializer_class = SQLUploadChunkSerializer


class SQLUploadMetadataViewSet(AuditBaseViewSet):
    """SQL Upload Metadata API."""
    queryset = SQLUploadMetadata.objects.prefetch_related(
        "upload_chunks"
    ).all()
    serializer_class = SQLUploadMetadataSerializer

    @action(
        detail=True,
        methods=["POST"],
        serializer_class=NewSQLUploadChunkSerializer
    )
    def start_chunk_upload(self, request: Request, pk) -> Response:
        """Start a new chunk upload."""
        self.check_object_permissions(request, request.user)
        serializer: NewSQLUploadChunkSerializer = self.get_serializer(
            data={
                **request.data,
                "upload_metadata": str(pk)
            }
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

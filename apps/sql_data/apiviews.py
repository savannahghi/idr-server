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


class SQLDatabaseViewSet(AuditBaseViewSet):
    """SQL Database Sources API."""
    queryset = SQLDatabaseSource.objects.all()
    serializer_class = SQLDatabaseSerializer


class SQLExtractMetadataViewSet(AuditBaseViewSet):
    """SQL Extract Metadata API."""
    queryset = SQLExtractMetadata.objects.prefetch_related(
        "applicable_source_versions", "data_source"
    ).all()
    serializer_class = SQLExtractMetadataSerializer


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

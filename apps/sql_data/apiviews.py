from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.views import Request, Response
from rest_framework.viewsets import GenericViewSet

from apps.core.apiviews import AuditBaseViewSet

from .filters import (
    DataSourceVersionFilter,
    SQLDatabaseSourceFilter,
    SQLExtractMetadataFilter,
    SQLUploadChunkFilter,
    SQLUploadMetadataFilter,
)
from .models import (
    DataSourceVersion,
    SQLDatabaseSource,
    SQLExtractMetadata,
    SQLUploadChunk,
    SQLUploadMetadata,
)
from .serializers import (
    DataSourceVersionSerializer,
    MarkUploadMetaAsCompleteSerializer,
    NewSQLUploadChunkSerializer,
    SQLDatabaseSerializer,
    SQLExtractMetadataSerializer,
    SQLUploadChunkSerializer,
    SQLUploadMetadataSerializer,
)


class DataSourceVersionViewSet(AuditBaseViewSet):
    """Data Source Version API."""

    queryset = DataSourceVersion.objects.all()
    serializer_class = DataSourceVersionSerializer
    filterset_class = DataSourceVersionFilter


class SQLDatabaseViewSet(AuditBaseViewSet):
    """SQL Database Sources API."""

    queryset = SQLDatabaseSource.objects.all()
    serializer_class = SQLDatabaseSerializer
    filterset_class = SQLDatabaseSourceFilter


class SQLExtractMetadataViewSet(AuditBaseViewSet):
    """SQL Extract Metadata API."""

    queryset = SQLExtractMetadata.objects.prefetch_related(
        "applicable_source_versions", "data_source"
    ).all()
    serializer_class = SQLExtractMetadataSerializer
    filterset_class = SQLExtractMetadataFilter


class SQLUploadChunkViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """SQL Upload Chunk API."""

    queryset = SQLUploadChunk.objects.all()
    serializer_class = SQLUploadChunkSerializer
    filterset_class = SQLUploadChunkFilter


class SQLUploadMetadataViewSet(AuditBaseViewSet):
    """SQL Upload Metadata API."""

    queryset = SQLUploadMetadata.objects.prefetch_related(
        "upload_chunks"
    ).all()
    serializer_class = SQLUploadMetadataSerializer
    filterset_class = SQLUploadMetadataFilter

    @action(
        detail=True,
        methods=["PATCH"],
        serializer_class=MarkUploadMetaAsCompleteSerializer,
    )
    def mark_as_complete(self, request: Request, pk) -> Response:
        """Mark this upload metadata as complete."""
        upload_meta: SQLUploadMetadata = self.get_object()
        upload_meta.mark_as_complete(user=request.user)
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["POST"],
        serializer_class=NewSQLUploadChunkSerializer,
    )
    def start_chunk_upload(self, request: Request, pk) -> Response:
        """Start a new chunk upload for this upload metadata."""
        self.check_object_permissions(request, request.user)
        serializer: NewSQLUploadChunkSerializer = self.get_serializer(
            data=request.data
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(upload_metadata=self.get_object())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

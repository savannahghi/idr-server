import os

from google.cloud import pubsub_v1
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.views import Request, Response
from rest_framework.viewsets import GenericViewSet

from apps.core.apiviews import AuditBaseViewSet
from utils.core_events import AbstractEventPublisher

from .models import (
    DataSourceVersion,
    SQLDatabaseSource,
    SQLExtractMetadata,
    SQLUploadChunk,
    SQLUploadMetadata,
)
from .serializers import (
    DataSourceVersionSerializer,
    NewSQLUploadChunkSerializer,
    SQLDatabaseSerializer,
    SQLExtractMetadataSerializer,
    SQLUploadChunkSerializer,
    SQLUploadMetadataSerializer,
)

publisher = pubsub_v1.PublisherClient()
topic_id = "idr_incoming_extracts_metadata"
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")


class DataSourceVersionViewSet(AuditBaseViewSet):
    """Data Source Version API."""

    queryset = DataSourceVersion.objects.all()
    serializer_class = DataSourceVersionSerializer
    filterset_fields = ["id", "data_source", "data_source_version"]


class SQLDatabaseViewSet(AuditBaseViewSet):
    """SQL Database Sources API."""

    queryset = SQLDatabaseSource.objects.all()
    serializer_class = SQLDatabaseSerializer
    filterset_fields = ["id", "name", "database_name", "database_vendor"]


class SQLExtractMetadataViewSet(AuditBaseViewSet):
    """SQL Extract Metadata API."""

    queryset = SQLExtractMetadata.objects.prefetch_related(
        "applicable_source_versions", "data_source"
    ).all()
    serializer_class = SQLExtractMetadataSerializer
    filterset_fields = [
        "id",
        "name",
        "data_source__database_name",
        "version",
        "preferred_uploads_name",
    ]


class SQLUploadChunkViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """SQL Upload Chunk API."""

    queryset = SQLUploadChunk.objects.all()
    serializer_class = SQLUploadChunkSerializer


class SQLUploadMetadataViewSet(AuditBaseViewSet, AbstractEventPublisher):
    """SQL Upload Metadata API."""

    queryset = SQLUploadMetadata.objects.prefetch_related(
        "upload_chunks"
    ).all()
    serializer_class = SQLUploadMetadataSerializer

    def publish_event(self, topic_path: str, data: bytes):
        future = publisher.publish(topic_path, data)
        print("Event publish result id ", future.result())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        topic_path = publisher.topic_path(project_id, topic_id)
        data = {
            "org_unit_name": serializer.validated_data.get("org_unit_name"),
            "org_unit_code": serializer.validated_data.get("org_unit_code"),
            "content_type": serializer.validated_data.get("content_type"),
            "extract_metadata": serializer.validated_data.get(
                "extract_metadata"
            ),
            "chunks": serializer.validated_data.get("chunks"),
        }

        # publish metadata upload success event
        self.publish_event(topic_path, str(data).encode("utf-8"))

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(
        detail=True,
        methods=["POST"],
        serializer_class=NewSQLUploadChunkSerializer,
    )
    def start_chunk_upload(self, request: Request, pk) -> Response:
        """Start a new chunk upload."""
        self.check_object_permissions(request, request.user)
        request.data["upload_metadata"] = str(pk)
        serializer: NewSQLUploadChunkSerializer = self.get_serializer(
            data=request.data
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

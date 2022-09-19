from apps.core.filters import AuditBaseFilterSet

from .models import (
    DataSourceVersion,
    SQLDatabaseSource,
    SQLExtractMetadata,
    SQLUploadChunk,
    SQLUploadMetadata,
)


class DataSourceVersionFilter(AuditBaseFilterSet):
    """Filter for the `DataSourceVersion` model."""

    class Meta:
        model = DataSourceVersion
        fields = ("id", "data_source", "data_source_version")


class SQLDatabaseSourceFilter(AuditBaseFilterSet):
    """Filter for the `SQLDatabaseSource` model."""

    class Meta:
        model = SQLDatabaseSource
        fields = ("id", "name", "database_name", "database_vendor")


class SQLExtractMetadataFilter(AuditBaseFilterSet):
    """Filter for the `SQLExtractMetadata` model."""

    class Meta:
        model = SQLExtractMetadata
        fields = (
            "id",
            "name",
            "data_source",
            "applicable_source_versions",
            "version",
            "preferred_uploads_name",
        )


class SQLUploadChunkFilter(AuditBaseFilterSet):
    """Filter for the `SQLUploadChunk` model."""

    class Meta:
        model = SQLUploadChunk
        fields = ("id", "upload_metadata")


class SQLUploadMetadataFilter(AuditBaseFilterSet):
    """Filter for the `SQLUploadMetadata` model."""

    class Meta:
        model = SQLUploadMetadata
        fields = {
            "id": ["exact"],
            "extract_metadata": ["exact"],
            "org_unit_code": ["exact"],
            "org_unit_name": ["exact", "icontains"],
            "start_time": ["exact", "lt", "gt"],
            "finish_time": ["exact", "lt", "gt"],
            "is_consumed": ["exact"],
        }

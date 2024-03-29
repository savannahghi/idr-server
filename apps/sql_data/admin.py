from django.contrib import admin

from apps.core.admin import AuditBaseModelAdmin

from .models import (
    DataSourceVersion,
    SQLDatabaseSource,
    SQLExtractMetadata,
    SQLUploadChunk,
    SQLUploadMetadata,
)


@admin.register(DataSourceVersion)
class DataSourceVersionAdmin(AuditBaseModelAdmin):
    list_display = ("data_source", "data_source_version")


@admin.register(SQLDatabaseSource)
class SQLDatabaseSourceAdmin(AuditBaseModelAdmin):
    list_display = ("name", "database_name", "database_vendor", "description")


@admin.register(SQLExtractMetadata)
class SQLExtractMetadataAdmin(AuditBaseModelAdmin):
    filter_horizontal = ("applicable_source_versions",)
    list_display = ("name", "version", "description")
    list_filter = ("data_source",)


@admin.register(SQLUploadChunk)
class SQLUploadChunkAdmin(AuditBaseModelAdmin):
    list_display = (
        "name",
        "upload_metadata",
        "chunk_index",
    )


@admin.register(SQLUploadMetadata)
class SQLUploadMetadataAdmin(AuditBaseModelAdmin):
    list_display = (
        "name",
        "data_source_name",
        "extract_metadata",
        "chunks_count",
        "start_time",
        "finish_time",
        "is_complete",
    )
    list_filter = ("extract_metadata", "org_unit_code", "org_unit_name")

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
    list_display = ("name", "version", "description")


@admin.register(SQLUploadChunk)
class SQLUploadChunk(AuditBaseModelAdmin):
    list_display = (
        "name", "upload_metadata", "chunk_index", "start_time", "finish_time",
        "is_complete"
    )


@admin.register(SQLUploadMetadata)
class SQLUploadMetadataAdmin(AuditBaseModelAdmin):
    list_display = (
        "name", "data_source_name", "made_on", "chunks", "is_complete"
    )

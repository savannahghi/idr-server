from apps.core.serializers import AuditBaseSerializer

from .models import (
    DataSourceVersion,
    SQLDatabaseSource,
    SQLExtractMetadata,
    SQLUploadChunk,
    SQLUploadMetadata
)


class DataSourceVersionSerializer(AuditBaseSerializer):

    class Meta:
        model = DataSourceVersion
        fields = "__all__"


class NewSQLUploadChunkSerializer(AuditBaseSerializer):

    class Meta:
        model = SQLUploadChunk
        fields = "__all__"


class SQLDatabaseSerializer(AuditBaseSerializer):

    class Meta:
        model = SQLDatabaseSource
        fields = "__all__"


class SQLExtractMetadataSerializer(AuditBaseSerializer):
    data_source = SQLDatabaseSerializer(read_only=True)
    applicable_source_versions = DataSourceVersionSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = SQLExtractMetadata
        fields = "__all__"


class SQLUploadChunkSerializer(NewSQLUploadChunkSerializer):

    class Meta(NewSQLUploadChunkSerializer.Meta):
        fields = "__all__"
        read_only_fields = ("upload_metadata",)


class SQLUploadMetadataSerializer(AuditBaseSerializer):
    upload_chunks = SQLUploadChunkSerializer(many=True, read_only=True)

    class Meta:
        model = SQLUploadMetadata
        fields = "__all__"

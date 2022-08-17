from rest_framework import serializers

from apps.core.serializers import AuditBaseSerializer

from .models import (
    DataSourceVersion,
    SQLDatabaseSource,
    SQLExtractMetadata,
    SQLUploadChunk,
    SQLUploadMetadata,
)


class MarkUploadMetaAsCompleteSerializer(serializers.Serializer):
    """Serializer used by the"""

    def create(self, validated_data):
        raise NotImplementedError("Not needed. Should never be called.")

    def update(self, instance, validated_data):
        raise NotImplementedError("Not needed. Should never be called.")


class NewSQLUploadChunkSerializer(AuditBaseSerializer):
    class Meta:
        model = SQLUploadChunk
        fields = ("id", "chunk_index", "chunk_content", "upload_metadata")
        read_only_fields = ("upload_metadata",)


class SQLDatabaseSerializer(AuditBaseSerializer):
    class Meta:
        model = SQLDatabaseSource
        fields = "__all__"


class DataSourceVersionSerializer(AuditBaseSerializer):
    data_source_detail = SQLDatabaseSerializer(
        read_only=True, source="data_source"
    )

    class Meta:
        model = DataSourceVersion
        fields = "__all__"


class SQLExtractMetadataSerializer(AuditBaseSerializer):
    data_source = SQLDatabaseSerializer(read_only=True)
    applicable_source_versions = DataSourceVersionSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = SQLExtractMetadata
        fields = "__all__"


class SQLUploadChunkSerializer(NewSQLUploadChunkSerializer):
    class Meta(NewSQLUploadChunkSerializer.Meta):
        fields = "__all__"
        read_only_fields = ("upload_metadata",)


class SQLUploadMetadataSerializer(AuditBaseSerializer):
    chunks_count = serializers.IntegerField(read_only=True)
    is_complete = serializers.BooleanField(read_only=True)
    upload_chunks = SQLUploadChunkSerializer(many=True, read_only=True)

    class Meta:
        model = SQLUploadMetadata
        fields = "__all__"
        read_only_fields = ("finish_time",)

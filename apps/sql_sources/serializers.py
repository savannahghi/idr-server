from apps.core.serializers import AuditBaseSerializer

from .models import SimpleSqlMetadata, SourceVersion


class SimpleSqlMetadataSerializer(AuditBaseSerializer):

    class Meta:
        model = SimpleSqlMetadata
        fields = "__all__"


class SourceVersionSerializer(AuditBaseSerializer):

    class Meta:
        model = SourceVersion
        fields = "__all__"

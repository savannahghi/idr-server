from django.db import models

from apps.core.models import AbstractMetadata, AuditBase, GenericSource


# =============================================================================
# MODELS
# =============================================================================

class AbstractSqlMetadata(AbstractMetadata):
    """Metadata to extract data from an sql database."""
    sql_query = models.TextField(
        null=False,
        blank=False,
        help_text=(
            "The actual SQL statement to be run against a database to "
            "retrieve data. Should be a valid SQL DML statement for the "
            "target database."
        )
    )

    class Meta:
        abstract = True


class SimpleSqlMetadata(AbstractSqlMetadata):
    source = models.ForeignKey(GenericSource, on_delete=models.PROTECT)
    applicable_versions = models.ManyToManyField("SourceVersion")


class SourceVersion(AuditBase):
    """Describes a version of a data source."""

    source = models.ForeignKey(GenericSource, on_delete=models.PROTECT)
    source_version = models.CharField(max_length=100)

    def __str__(self) -> str:
        return "%s v(%s)" % (self.source, self.source_version)

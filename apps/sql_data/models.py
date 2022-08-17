from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import (
    AbstractDataSource,
    AbstractExtractMetadata,
    AbstractOrgUnitUploadMetadata,
    AbstractUploadChunk,
    AuditBase,
)

# =============================================================================
# HELPERS
# =============================================================================


def sql_extracts_upload_to(instance: "SQLUploadChunk", filename: str) -> str:
    ex_meta: SQLExtractMetadata = instance.upload_metadata.extract_metadata
    extracts_group_name: str = ex_meta.preferred_uploads_name or ex_meta.name
    return "%s/%s/%s/%s/%d__%s" % (
        settings.BASE_EXTRACTS_UPLOAD_DIR_NAME,
        settings.SQL_EXTRACTS_UPLOAD_DIR_NAME,
        extracts_group_name,
        instance.upload_metadata.name,
        instance.chunk_index,
        str(instance.pk),
    )


# =============================================================================
# MODELS
# =============================================================================


class DataSourceVersion(AuditBase):
    """Describes a version of a data source.

    Note that this can either be the version of the database or the version of
    the system for which the source database belongs to.
    """

    data_source = models.ForeignKey(
        "SQLDatabaseSource", on_delete=models.PROTECT
    )
    data_source_version = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return "%s v(%s)" % (str(self.data_source), self.data_source_version)


class SQLDatabaseSource(AbstractDataSource):
    """This represents an SQL database as a data source."""

    class DatabaseVendors(models.TextChoices):
        """The supported database vendors."""

        MYSQL = "mysql", _("MySQL")
        POSTGRES_SQL = "postgres", _("Postgres SQL")

    database_name = models.CharField(
        max_length=255,
        help_text=_(
            "This is a hint as to the source database to use. Since it might "
            "not always be possible to know the exact name of the source "
            "database, as this might be configuration dependent, this should "
            "be thought of as a hint to the client on the database to use for "
            "the extraction."
        ),
    )
    database_vendor = models.CharField(
        max_length=20,
        choices=DatabaseVendors.choices,
        default=DatabaseVendors.MYSQL.value,
    )


class SQLExtractMetadata(AbstractExtractMetadata):
    """This represents extract metadata for SQL database sources."""

    sql_query = models.TextField(
        null=False,
        blank=False,
        help_text=_(
            "The actual SQL statement to be run against a database to "
            "retrieve data. Should be a valid SQL DML statement for the "
            "target database."
        ),
    )
    data_source = models.ForeignKey(
        SQLDatabaseSource,
        on_delete=models.PROTECT,
        related_name="available_extracts",
    )
    applicable_source_versions = models.ManyToManyField(
        DataSourceVersion,
        related_name="available_versions",
        verbose_name=_("Applicable data source versions"),
    )
    extras = models.JSONField(
        blank=True, default=dict, help_text=_("Extra metadata.")
    )

    class Meta(AbstractExtractMetadata.Meta):
        verbose_name_plural = "Sql extract metadata"


class SQLUploadChunk(AbstractUploadChunk):
    """Represents a segment of data being uploaded from an SQL database."""

    upload_metadata = models.ForeignKey(
        "SQLUploadMetadata",
        on_delete=models.PROTECT,
        related_name="upload_chunks",
    )
    chunk_content = models.FileField(
        upload_to=sql_extracts_upload_to,
        max_length=4096,
        null=True,
        blank=True,
    )

    @property
    def name(self) -> str:
        """A name for this chunk."""
        return "%d__%s" % (self.chunk_index, str(self.pk))

    def __str__(self) -> str:
        return self.name


class SQLUploadMetadata(AbstractOrgUnitUploadMetadata):
    """This represents an upload of data extracted from an SQL database."""

    class UploadContentTypes(models.TextChoices):
        """The supported content types for the upload data."""

        CSV = "text/csv", _("CSV")
        JSON = "application/json", _("JSON")
        MS_EXCEL = "application/vnd.ms-excel", _("MS Excel")
        MS_EXCEL_07 = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # noqa
            _("MS Excel 2007 and Later"),
        )
        PARQUET = "application/vnd.apache-parquet", _("Parquet")

    extract_metadata = models.ForeignKey(
        SQLExtractMetadata, on_delete=models.PROTECT, related_name="uploads"
    )
    content_type = models.CharField(
        max_length=100, choices=UploadContentTypes.choices
    )
    is_consumed = models.BooleanField(
        editable=False,
        default=False,
        blank=True,
        help_text=_(
            "Indicates that the concerned parties have received the uploaded "
            "data, and it's safe for the server to clear out the uploaded "
            "files(should it choose to) for efficiency reasons."
        ),
    )
    extras = models.JSONField(
        blank=True, default=dict, help_text=_("Extra metadata.")
    )

    @property
    def chunks_count(self) -> int:
        return self.upload_chunks.count()  # noqa

    @property
    def data_source_name(self) -> str:
        """Return the name of the source of thus upload."""
        return self.extract_metadata.data_source.name

    def mark_as_complete(self, user=None) -> None:
        self.update(modifier=user, finish_time=timezone.now())
        # TODO: Add an action to notify interested parties.

    class Meta(AbstractExtractMetadata.Meta):
        verbose_name_plural = "Sql upload metadata"

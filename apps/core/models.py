"""
This module contains the essential components and classes used through out
this project. It also defines the core abstractions that describe the essence
of this project.

Most of the core abstractions defined here are thin skeletons that describe the
minimal aspects of a domain and are meant to be work together to produce a
working process. However, these relationships aren't expressed in the
abstractions(this is due to the limitations of django) but are documented on
the abstractions themselves.
"""
import uuid
from django.db import models
from typing import TypeVar

from django.conf import settings
from django.utils.translation import gettext_lazy as _

# =============================================================================
# TYPES
# =============================================================================

BM = TypeVar("BM", bound="BaseModel", covariant=True)


# =============================================================================
# QUERY SETS
# =============================================================================

class BaseQuerySet(models.QuerySet[BM]):
    """This is the base `QuerySet` used in the project."""
    ...


# =============================================================================
# MANAGERS
# =============================================================================

class BaseManager(models.Manager[BM]):
    """This is the default `Manager` for all models in this project."""
    use_for_related_fields = True
    use_in_migrations = True

    def get_queryset(self) -> BaseQuerySet:
        """
        Returns a `QuerySet` instance to use with this manager. All `QuerySet`
        instances returned by this method are instances of `BaseQuerySet`.

        :return: a QuerySet instance.
        """
        return BaseQuerySet(self.model, using=self._db)


class AuditBaseManager(BaseManager):
    """This is the default manager for all `AuditBase` models."""
    use_for_related_fields = True
    use_in_migrations = True

    def create(self, creator=None, **kwargs):
        """
        Creates a new `AuditBase` instance with the given properties and by
        the given `User`. Returns the created instance.

        :param creator: The User who initiated this create action/request.
        :param kwargs: A dict of properties to pass to the object being
               created.
        :return: The created instance.
        """
        kwargs.setdefault("created_by", creator)
        instance = super().create(**kwargs)
        return instance


# =============================================================================
# BASE MODELS
# =============================================================================

class BaseModel(models.Model):
    """
    This is the base `Model` of the project from which all concrete inherit
    from.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Default Manager
    objects: BaseManager = BaseManager()

    class Meta:
        abstract = True


class AuditBase(BaseModel):
    """
    This is the base `Model` from which all auditable models are derived from.
    """
    # Instance creation data
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.PROTECT,
        related_name="%(app_label)s_%(class)s_created_by",
        null=True, db_column="created_by", blank=True, editable=False
    )
    # Instance modification data
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.PROTECT,
        related_name="%(app_label)s_%(class)s_updated_by",
        null=True, db_column="updated_by", blank=True, editable=False
    )
    # Default Manager
    objects: AuditBaseManager = AuditBaseManager()

    def save(self, user=None, *args, **kwargs):
        """
        Persist the calling instance into the database and also record it's
        creator or modifier. If the `user` param is provided and this is the
        first time saving of this instance, then the user is marked as the
        creator of the object, otherwise the user is marked as the last
        modifier of this instance.

        :param user The creator or modifier of this instance.
        """
        # If this is the first time saving this instance and a user has been
        # provided, then mark the user as the creator of the instance.
        if self.pk is None and user:
            self.created_by = user
        # Else if a user has been provided mark the user as the modifier of
        # the object
        elif user:
            self.updated_by = user
        # Finish by saving the model instance
        super().save(*args, **kwargs)

    def update(self, modifier=None, **kwargs) -> "AuditBase":
        """
        This method takes the fields to update plus their values as key word
        arguments and updates this instance to match that state. This is the
        preferred method of updating **AuditBase** instances. This method
        takes the user performing the update as the first parameter and marks
        the user as the last modifier of this instance. The following
        conditions hold:

        * If no key word arguments are provided, then no updates should be
          performed, including the object's last update status and the object
          should remain as is.
        * Only the fields included in the *kwargs* argument are updated.

        :param modifier: The user who initiated the update action/request.
        :param kwargs: A dict of the instance fields and value to update with.

        :return: the updated instance.
        """
        # If no key word arguments were provided, don't perform any updates,
        # return the object as is.
        if len(kwargs) == 0:
            return self

        # Update this object to match the given state
        for field, value in kwargs.items():
            setattr(self, field, value)

        # TODO: Add support for many to many fields

        # Update only the fields provided
        updatable_fields = (*kwargs.keys(), 'updated_by')
        self.save(modifier, update_fields=updatable_fields)
        return self

    class Meta(BaseModel.Meta):
        abstract = True
        get_latest_by = ("-updated_at", "-created_at")
        ordering = ("-updated_at", "-created_at")


# =============================================================================
# CORE ABSTRACTIONS
# =============================================================================

class AbstractDataSource(AuditBase):
    """
    Represents a data source.

    This is a data source for the sake of recording keeping(doesn't have to be
    a database, but rather could be the system using the db).

    A source can have multiple extract metadata.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return self.name

    class Meta(AuditBase.Meta):
        abstract = True


class AbstractUploadChunk(AuditBase):
    """Represents an upload chunk.

    This class is intended to be used together with the
    `AbstractUploadMetadata` instances. That is, each upload will be composed
    of multiple chunks.
    """
    start_time = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text=_("The time the upload of this chunk commenced.")
    )
    finish_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_(
            "The completion time of the upload this chunk. An upload will "
            "only be considered complete once this value is non-null."
        )
    )
    chunk_index = models.PositiveIntegerField()

    @property
    def is_complete(self) -> bool:
        """Return true if this chunk has been uploaded completely.

        For this implementation, a chunk is considered complete if it's finish
        date is not None.
        """
        return getattr(self, "finish_time", None) is not None

    class Meta(AuditBase.Meta):
        abstract = True


class AbstractExtractMetadata(AuditBase):
    """Metadata that describes the data to be extracted by clients.

    Each extract is only applicable to a single a source.
    """
    name = models.CharField(max_length=200)
    version = models.CharField(
        max_length=100,
        help_text="The version of this metadata."
    )
    description = models.TextField(blank=True, default="")
    preferred_uploads_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text=_(
            "A name that all uploads relating to this extract should have or "
            "be grouped by. Note that the final name is dependent on the "
            "upload metadata implementation in use and thus this is more of a "
            "hint(to upload metadata implementations) of a suitable name to "
            "use."
        )
    )

    def __str__(self) -> str:
        return self.name

    class Meta(AuditBase.Meta):
        abstract = True


class AbstractUploadMetadata(AuditBase):
    """Metadata that describes a data upload by a client."""
    made_on = models.DateTimeField(auto_now_add=True, editable=False)
    chunks = models.PositiveIntegerField(
        default=1,
        help_text=_("The number of chunks contained in this upload.")
    )

    @property
    def is_complete(self) -> bool:
        """Return true if this upload completed successfully, false otherwise.

        An upload is considered successful if all the chunks for the upload
        have been uploaded successfully.
        """
        raise NotImplementedError("`is_compete` must be implemented.")

    @property
    def name(self) -> str:
        """Return a name for this upload."""
        raise NotImplementedError("`name` must be implemented.")

    def __str__(self) -> str:
        return self.name

    class Meta(AuditBase.Meta):
        abstract = True


class AbstractOrgUnitUploadMetadata(AbstractUploadMetadata):  # noqa
    """Extends `AbstractUploadMetadata` to also capture location data.

    The location is expected to have a code to ease indexing and a human
    readable name.
    """
    org_unit_code = models.CharField(
        max_length=150,
        help_text=_(
            "This is a code representing the location from which this upload "
            "was made. E.g, an MFL code for facilities in Kenya."
        )
    )
    org_unit_name = models.CharField(
        max_length=250,
        help_text=_(
            "A human-readable name for the location from which this upload "
            "was made. E.g, the name of a facility."
        )
    )

    @property
    def name(self) -> str:
        """Return a name for this upload."""
        return "%s__%s__%s__%s" % (
            self.org_unit_code,
            self.org_unit_name,
            str(self.made_on),
            str(self.pk)
        )

    class Meta(AbstractUploadMetadata.Meta):
        abstract = True

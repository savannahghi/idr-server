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
        :param args: A tuple of properties to pass to the object being created.
        :param kwargs: A dict of properties to pass to the object being created.
        :return: The created instance.
        """
        kwargs.setdefault("created_by", creator)
        instance = super().create(**kwargs)
        return instance


# =============================================================================
# MODELS
# =============================================================================

class BaseModel(models.Model):
    """
    This is the base `Model` of the project from which all concrete inherit
    from.
    """
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

    class Meta:
        abstract = True


class AbstractSource(AuditBase):
    """
    Represents a data source.

    This is a data source for the sake of recording keeping(doesn't have to be
    a database, but rather could be the system using the db).
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True


class AbstractMetadata(AuditBase):
    """Metadata that describes the data to be extracted by clients."""
    name = models.CharField(max_length=200)
    version = models.CharField(
        max_length=100,
        help_text="The version of this metadata."
    )
    description = models.TextField(blank=True, default="")
    extract_name = models.CharField(max_length=200, null=True, blank=True)
    # meta_source = models.ForeignKey()

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True


class GenericSource(AbstractSource):
    """This is a generic data source."""
    ...

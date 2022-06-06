from typing import Any, Dict, Optional

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import AuditBase

User = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    """
    This is the root `Serializer` from which all other serializers in the
    project are derived from.
    """

    class Meta:
        abstract = True


class AuditBaseSerializer(BaseSerializer):
    """
    This is the base `Serializer` for all `AuditBase` models in this project.
    Audit data is only available to admin users.
    """

    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only show audit data to admin users
        user = self.get_user_from_context()
        if not (user and user.is_staff):  # type: ignore
            for field in ("created_by", "updated_at", "updated_by"):
                self.fields.pop(field, None)

    def create(self, validated_data: Dict) -> AuditBase:
        """
        Creates and returns a new model instance with the provided validated
        data. This implementation also adds the user who made the create
        request as the "creator" of the object if such a user is present.

        :param validated_data: The validated data to use when creating the
        instance.

        :return: the created instance.
        """
        user = self.get_user_from_context()
        validated_data["creator"] = user
        return super().create(validated_data)

    def get_user_from_context(self) -> Optional[User]:
        """
        Finds and returns the user attached to this serializer's context or
        None if the user isn't found.

        :return: the user attached to this serializer's context or None if the
        user isn't found.
        """
        request = self.context.get("request", None)
        return request.user if request else None

    def update(
        self, instance: AuditBase, validated_data: Dict[str, Any]
    ) -> AuditBase:
        """
        Updates and returns the given instance with the given validated data.
        This implementation also adds the user who made the update request as
        the "modifier" of the object if such a user is present.

        :param instance: The instance to update.
        :param validated_data: The validated data to use when updating the
        instance.

        :return: the updated instance.
        """
        user = self.get_user_from_context()
        validated_data["modifier"] = user
        return instance.update(**validated_data)

    class Meta(BaseSerializer.Meta):
        abstract = True

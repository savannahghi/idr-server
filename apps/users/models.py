import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# =============================================================================
# MODELS
# =============================================================================

class User(AbstractUser):
    """Default user model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_approved = models.BooleanField(
        default=False,
        help_text=(
            "When true, the user is able to log in to the main website (and "
            "vice versa)"
        )
    )
    approval_notified = models.BooleanField(
        default=False,
        help_text=(
            "When true, the user has been notified that their account is "
            "approved"
        ),
    )

    @property
    def name(self) -> str:
        return self.get_full_name()

    def __str__(self) -> str:
        return self.name

    class Meta(AbstractUser.Meta):
        permissions = [
            ("can_view_dashboard", "Can View Dashboard"),
        ]

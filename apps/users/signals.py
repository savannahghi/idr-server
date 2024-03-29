from typing import Sequence

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

# =============================================================================
# TYPES
# =============================================================================

User = get_user_model()


# =============================================================================
# CONSTANTS
# =============================================================================

BASIC_PERMISSIONS: Sequence[str] = ("users.can_view_dashboard",)


# =============================================================================
# ACTIONS AND SIGNALS
# =============================================================================


def assign_basic_permissions(user: User) -> None:
    for perm_string in BASIC_PERMISSIONS:
        content_type_app_label, perm_code_name = perm_string.split(".")
        perm = Permission.objects.get(
            codename=perm_code_name,
            content_type__app_label=content_type_app_label,
        )
        user.user_permissions.add(perm)  # type: ignore

    user.save()


@receiver(post_save, sender=User)
def account_confirmed_handler(sender, instance, created, **kwargs):
    if created:
        assign_basic_permissions(instance)

    return True

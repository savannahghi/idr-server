import factory
from django.contrib.auth import get_user_model

# =============================================================================
# TYPES
# =============================================================================

User = get_user_model()


# =============================================================================
# FACTORIES
# =============================================================================


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for `app.users.models.User` model."""

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.LazyAttribute(lambda u: "%s@example.test" % u.username)
    password = factory.PostGenerationMethodCall("set_password", "ChangeMe12!!")
    is_staff = False

    class Meta:
        model = User
        django_get_or_create = ("username",)


class AdminFactory(factory.django.DjangoModelFactory):
    """Factory for `app.users.models.User` model.

    Each instance created using this factory will have it's *is_staff* method
    set to `True`.
    """

    username = factory.Sequence(lambda n: "admin%d" % n)
    is_staff = True

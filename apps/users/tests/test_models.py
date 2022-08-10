from django.test import TestCase

from apps.users.models import User

from .factories import UserFactory


class UserTest(TestCase):
    """Tests for the `User` model."""

    def setUp(self) -> None:
        super().setUp()
        self.user: User = UserFactory.create(
            first_name="Juha", last_name="Kalulu"
        )

    def test_name_property(self) -> None:
        """Test  the `self.name` property."""
        assert self.user.name == "Juha Kalulu"

    def test_representation(self) -> None:
        """Test the `self.__str()__` method."""
        assert str(self.user) == "Juha Kalulu"

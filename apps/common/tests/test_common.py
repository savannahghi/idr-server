import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from faker import Faker
from rest_framework.test import APIRequestFactory, APITestCase

fake = Faker()
factory = APIRequestFactory()


class LoggedInMixin(APITestCase):
    """A mixin for user to be used across these tests."""

    def setUp(self):
        """Create a test user for the logged-in session."""
        super(LoggedInMixin, self).setUp()
        username = str(uuid.uuid4())
        self.user = get_user_model().objects.create_superuser(
            email=fake.email(),
            password="pass@123",
            username=username,
        )
        all_perms = Permission.objects.all()
        for perm in all_perms:
            self.user.user_permissions.add(perm)
        self.user.save()

        assert (
            self.client.login(username=username, password="pass@123") is True
        )

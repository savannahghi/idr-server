import pytest
from faker import Faker
from rest_framework.test import APITestCase
from sghi.idr_server.test import LoggedInMixin

from sghi.idr_server.apps.users.signals import assign_basic_permissions

pytestmark = pytest.mark.django_db

fake = Faker()


class TestSignals(LoggedInMixin, APITestCase):
    def test_assign_permissions(self):
        assign_basic_permissions(self.user)
        assert self.user.get_all_permissions() is not None

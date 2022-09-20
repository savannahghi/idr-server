import pytest
from faker import Faker
from rest_framework.test import APITestCase

from apps.common.tests.test_common import LoggedInMixin
from apps.users.signals import assign_basic_permissions

pytestmark = pytest.mark.django_db

fake = Faker()


class TestSignals(LoggedInMixin, APITestCase):
    def test_assign_permissions(self):
        assign_basic_permissions(self.user)
        assert self.user.get_all_permissions() is not None

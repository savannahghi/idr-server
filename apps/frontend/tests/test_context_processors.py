import pytest
from faker import Faker
from rest_framework.test import APIRequestFactory, APITestCase

from apps.common.tests.test_common import LoggedInMixin
from apps.frontend.context_processors import dashboards

pytestmark = pytest.mark.django_db

fake = Faker()


class InitializeTestData(LoggedInMixin, APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        super().setUp()

    def test_context_processor_dashboards_as_staff(self):
        request = self.factory.request()
        request.user = self.user
        response = dashboards(request)
        assert response.get("dashboards") != ""

    def test_context_processor_dashboards_as_non_staff(self):
        request = self.factory.request()
        request.user = self.user
        request.user.is_staff = False
        response = dashboards(request)
        assert len(response.get("dashboards")) >= 0

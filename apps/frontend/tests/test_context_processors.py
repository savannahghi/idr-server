import pytest
from faker import Faker
from model_bakery import baker
from rest_framework.test import APIRequestFactory, APITestCase

from apps.common.tests.test_common import LoggedInMixin
from apps.dashboards.models import Dashboard
from apps.frontend.context_processors import dashboards

pytestmark = pytest.mark.django_db

fake = Faker()


class TestContextProcessors(LoggedInMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.dashboard = baker.make(Dashboard)

    def test_context_processor_dashboards_as_staff(self):
        request = self.factory.request()
        request.user = self.user
        response = dashboards(request)
        assert response.get("dashboards") is not None

    def test_context_processor_dashboards_as_non_staff(self):
        request = self.factory.request()
        request.user = self.user
        request.user.is_staff = False
        response = dashboards(request)
        assert len(response.get("dashboards")) >= 0

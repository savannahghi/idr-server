import pytest
from faker import Faker
from model_bakery import baker
from rest_framework.test import APITestCase

from apps.common.tests.test_common import LoggedInMixin
from apps.dashboards.models import Dashboard, Visualization

pytestmark = pytest.mark.django_db

fake = Faker()


class TestDashboardModels(LoggedInMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.dashboard = baker.make(Dashboard)
        self.visualization = baker.make(Visualization)

    def test_dashboard_str(self):
        assert str(self.dashboard) == str(self.dashboard.title)

    def test_visualization_str(self):
        assert str(self.visualization) == str(self.visualization.title)

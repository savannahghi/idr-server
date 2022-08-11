from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework.test import APIRequestFactory, APITestCase

from apps.common.tests.test_common import LoggedInMixin
from apps.dashboards.models import Dashboard, Visualization

fake = Faker()
factory = APIRequestFactory()


class TestVisualizationViewSet(LoggedInMixin, APITestCase):
    def setUp(self):
        self.visualization = baker.make(Visualization)
        super().setUp()

    def test_create(self):
        data = {
            "title": self.visualization.title,
            "description": self.visualization.description,
            "source": self.visualization.source,
            "width": self.visualization.width,
            "height": self.visualization.height,
            "weight": self.visualization.weight,
            "is_published": self.visualization.is_published,
        }
        url = reverse("visualization-list")
        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_get(self):
        fake_data = baker.make(Visualization)
        url = reverse("visualization-detail", kwargs={"pk": fake_data.id})
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_all(self):
        url = reverse("visualization-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_update(self):
        fake_data = baker.make(Visualization)
        url = reverse("visualization-detail", kwargs={"pk": fake_data.id})
        response = self.client.patch(url, {"title": "updated title"})
        assert response.status_code == 200

    def test_delete(self):
        fake_data = baker.make(Visualization)
        url = reverse("visualization-detail", kwargs={"pk": fake_data.id})
        response = self.client.delete(url)
        assert response.status_code == 204


class TestDashboardViewSet(LoggedInMixin, APITestCase):
    def setUp(self):
        self.dashboard = baker.make(Dashboard)
        super().setUp()

    def test_create(self):
        data = {
            "title": self.dashboard.title,
            "description": self.dashboard.description,
            "layout": self.dashboard.layout,
            "weight": self.dashboard.weight,
            "visualizations": self.dashboard.visualizations,
        }
        url = reverse("dashboard-list")
        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_get(self):
        fake_data = baker.make(Dashboard)
        url = reverse("dashboard-detail", kwargs={"pk": fake_data.id})
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_all(self):
        url = reverse("dashboard-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_update(self):
        fake_data = baker.make(Dashboard)
        url = reverse("dashboard-detail", kwargs={"pk": fake_data.id})
        response = self.client.patch(url, {"title": "updated title"})
        assert response.status_code == 200

    def test_delete(self):
        fake_data = baker.make(Dashboard)
        url = reverse("dashboard-detail", kwargs={"pk": fake_data.id})
        response = self.client.delete(url)
        assert response.status_code == 204

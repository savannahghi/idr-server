from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework.test import (
    APIRequestFactory,
    APITestCase,
    force_authenticate,
)

from apps.common.tests.test_common import LoggedInMixin
from apps.dashboards.apiviews import DashboardViewSet, VisualizationViewSet
from apps.dashboards.models import Dashboard, Visualization

fake = Faker()


class TestVisualizationViewSet(LoggedInMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.visualization_1 = baker.make(Visualization)
        self.visualization_2 = baker.make(Visualization, is_published=True)

    def test_create(self):
        data = {
            "title": self.visualization_1.title,
            "description": self.visualization_1.description,
            "source": self.visualization_1.source,
            "width": self.visualization_1.width,
            "height": self.visualization_1.height,
            "weight": self.visualization_1.weight,
            "is_published": self.visualization_1.is_published,
        }
        url = reverse("visualization-list")
        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_get(self):
        fake_data = baker.make(Visualization)
        url = reverse("visualization-detail", kwargs={"pk": fake_data.id})
        response = self.client.get(url)
        assert not response.data["is_published"]
        assert response.status_code == 200

    def test_list_view(self):
        url = reverse("visualization-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_list_view_as_staff(self):
        request = self.factory.get(
            reverse("visualization-list"),
        )
        request.user = self.user
        request.user.is_staff = True
        view = VisualizationViewSet.as_view(actions={"get": "list"})
        response = view(request)
        assert self.user.is_staff
        assert response.data["count"] == 2
        assert response.status_code == 200

    def test_list_view_as_non_staff(self):
        request = self.factory.get(
            reverse("visualization-list"),
        )
        request.user = self.user
        request.user.is_staff = False
        view = VisualizationViewSet.as_view(actions={"get": "list"})
        response = view(request)
        assert not self.user.is_staff
        assert response.data["count"] == 1
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
        super().setUp()
        self.factory = APIRequestFactory()
        self.dashboard_1 = baker.make(Dashboard)
        self.dashboard_2 = baker.make(Dashboard, is_published=True)

    def test_create(self):
        data = {
            "title": self.dashboard_1.title,
            "description": self.dashboard_1.description,
            "layout": self.dashboard_1.layout,
            "weight": self.dashboard_1.weight,
            "visualizations": self.dashboard_1.visualizations,
        }
        url = reverse("dashboard-list")
        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_get(self):
        fake_data = baker.make(Dashboard)
        url = reverse("dashboard-detail", kwargs={"pk": fake_data.id})
        response = self.client.get(url)
        assert not response.data["is_published"]
        assert response.status_code == 200

    def test_list_view(self):
        url = reverse("dashboard-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_list_view_as_staff(self):
        request = self.factory.get(
            reverse("dashboard-list"),
        )
        request.user = self.user
        request.user.is_staff = True
        view = DashboardViewSet.as_view(actions={"get": "list"})
        response = view(request)
        assert self.user.is_staff
        assert response.data["count"] == 2
        assert response.status_code == 200

    def test_list_view_as_non_staff(self):
        request = self.factory.get(
            reverse("dashboard-list"),
        )
        request.user = self.user
        request.user.is_staff = False
        view = DashboardViewSet.as_view(actions={"get": "list"})
        force_authenticate(request, user=self.user)
        response = view(request)
        assert not self.user.is_staff
        assert response.data["count"] == 1
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

import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework.test import APIRequestFactory, APITestCase

from apps.common.models import GenericSource
from apps.sql_data.models import SQLUploadChunk, SQLUploadMetadata
from apps.dashboards.models import Dashboard, Visualization

fake = Faker()
factory = APIRequestFactory()


class LoggedInMixin(APITestCase):
    """A mixin for user to be used across these tests. """

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

        assert self.client.login(username=username, password="pass@123") is True


class TestGenericSourceViewSet(LoggedInMixin, APITestCase):
    def setUp(self):
        self.generic_source = baker.make(GenericSource, description=fake.text())
        super().setUp()

    def test_create(self):
        data = {
            "name": fake.name(),
            "description": fake.text()
        }
        url = reverse("genericsource-list")
        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_get(self):
        fake_data = baker.make(GenericSource, name=fake.name(),
                               description=fake.text())
        url = reverse("genericsource-detail", kwargs={"pk": fake_data.id})
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_all(self):
        url = reverse("genericsource-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_update(self):
        fake_data = baker.make(GenericSource, name=fake.name(),
                               description=fake.text())
        url = reverse("genericsource-detail", kwargs={"pk": fake_data.id})
        response = self.client.patch(url, {"name": "changed name"})
        assert response.status_code == 200

    def test_delete(self):
        fake_data = baker.make(GenericSource, name=fake.name(),
                               description=fake.text())
        url = reverse("genericsource-detail", kwargs={"pk": fake_data.id})
        response = self.client.delete(url)
        assert response.status_code == 204


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
            "is_published": self.visualization.is_published
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
            "visualizations": self.dashboard.visualizations
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


class TestSQLUploadChunkViewSet(LoggedInMixin, APITestCase):
    def setUp(self):
        self.sql_upload_chunk = baker.make(SQLUploadChunk)
        super().setUp()

    def test_get(self):
        fake_data = baker.make(SQLUploadChunk)
        url = reverse("sqluploadchunk-detail", kwargs={"pk": fake_data.id})
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_all(self):
        url = reverse("sqluploadchunk-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_update(self):
        fake_data = baker.make(SQLUploadChunk)
        url = reverse("sqluploadchunk-detail", kwargs={"pk": fake_data.id})
        response = self.client.patch(url, {"chunk-index": 4})
        assert response.status_code == 200


class TestSQLUploadMetadataViewSet(LoggedInMixin, APITestCase):
    def setUp(self):
        self.upload_metadata = baker.make(SQLUploadMetadata)
        super().setUp()

    def test_create(self):
        data = {
            "chunk_index": 1
        }
        url = reverse("sqluploadmetadata-start-chunk-upload", kwargs={"pk": self.upload_metadata.pk})
        response = self.client.post(url, data, format="json")
        assert response.status_code == 201


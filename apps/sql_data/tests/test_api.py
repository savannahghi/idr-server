from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework.test import APIRequestFactory, APITestCase

from apps.common.tests.test_common import LoggedInMixin
from apps.sql_data.models import SQLUploadChunk, SQLUploadMetadata

fake = Faker()
factory = APIRequestFactory()


class TestSQLUploadChunkViewSet(LoggedInMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.sql_upload_chunk = baker.make(SQLUploadChunk)

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

    def test_start_chunk_upload_success(self):
        upload_metadata = baker.make(SQLUploadMetadata)
        data = {"chunk_index": 2}
        url = reverse(
            "sqluploadmetadata-start-chunk-upload",
            kwargs={"pk": upload_metadata.id},
        )
        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_start_chunk_upload_fail(self):
        upload_metadata = baker.make(SQLUploadMetadata)
        data = {"bad_data": 4}
        url = reverse(
            "sqluploadmetadata-start-chunk-upload",
            kwargs={"pk": upload_metadata.id},
        )
        response = self.client.post(url, data)
        assert response.status_code == 400


class TestSQLUploadMetadataViewSet(LoggedInMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.upload_metadata = baker.make(SQLUploadMetadata)

    def test_create(self):
        data = {"chunk_index": 1}
        url = reverse(
            "sqluploadmetadata-start-chunk-upload",
            kwargs={"pk": self.upload_metadata.pk},
        )
        response = self.client.post(url, data, format="json")
        assert response.status_code == 201

    def test_upload_completion(self):
        data = {"chunk_index": 1}
        url = reverse(
            "sqluploadmetadata-mark-as-complete",
            kwargs={"pk": self.upload_metadata.pk},
        )
        response = self.client.patch(url, data, format="json")
        assert response.status_code == 200

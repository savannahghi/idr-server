from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework.test import APITestCase

from apps.common.models import GenericSource
from apps.common.tests.test_common import LoggedInMixin

fake = Faker()


class TestGenericSourceViewSet(LoggedInMixin, APITestCase):
    def setUp(self):
        self.generic_source = baker.make(
            GenericSource, description=fake.text()
        )
        super().setUp()

    def test_create(self):
        data = {"name": fake.name(), "description": fake.text()}
        url = reverse("genericsource-list")
        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_get(self):
        fake_data = baker.make(
            GenericSource, name=fake.name(), description=fake.text()
        )
        url = reverse("genericsource-detail", kwargs={"pk": fake_data.id})
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_all(self):
        url = reverse("genericsource-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_update(self):
        fake_data = baker.make(
            GenericSource, name=fake.name(), description=fake.text()
        )
        url = reverse("genericsource-detail", kwargs={"pk": fake_data.id})
        response = self.client.patch(url, {"name": "changed name"})
        assert response.status_code == 200

    def test_delete(self):
        fake_data = baker.make(
            GenericSource, name=fake.name(), description=fake.text()
        )
        url = reverse("genericsource-detail", kwargs={"pk": fake_data.id})
        response = self.client.delete(url)
        assert response.status_code == 204

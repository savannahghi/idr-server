import pytest
from django.conf import settings
from django.test import TestCase
from faker import Faker
from model_bakery import baker

from apps.sql_data.models import SQLDatabaseSource
from apps.users.models import User

fake = Faker()
pytestmark = pytest.mark.django_db


class AuditBaseModelTest(TestCase):
    """Test for AuditBase."""

    def setUp(self):
        super().setUp()
        self.user = baker.make(settings.AUTH_USER_MODEL, email=fake.email())

    def test_created_and_created_by(self):
        sql_upload_metadata = SQLDatabaseSource(
            pk=None,
            name=fake.name(),
            description=fake.text(),
            database_name="sql",
            database_vendor="MySQL",
        )
        sql_upload_metadata.save(user=User.objects.get(pk=self.user.pk))
        assert sql_upload_metadata.created_by == self.user
        assert sql_upload_metadata.updated_by is None

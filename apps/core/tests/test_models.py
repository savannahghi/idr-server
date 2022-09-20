from datetime import datetime

import pytest
from django.conf import settings
from django.test import TestCase
from faker import Faker
from model_bakery import baker

from apps.sql_data.models import (
    SQLDatabaseSource,
    SQLExtractMetadata,
    SQLUploadMetadata,
)
from apps.users.models import User

fake = Faker()
pytestmark = pytest.mark.django_db


class TestAuditBase(TestCase):
    """Test class: AuditBase."""

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


class TestAbstractExtractMetadata(TestCase):
    """Test class: AbstractExtractMetadata."""

    def setUp(self):
        super().setUp()
        self.user = baker.make(settings.AUTH_USER_MODEL, email=fake.email())
        self.sql_extract_metadata = baker.make(SQLExtractMetadata)

    def test_default_str(self):
        assert str(self.sql_extract_metadata) == str(
            self.sql_extract_metadata.name
        )


class TestAbstractUploadMetadata(TestCase):
    """Test class: AbstractUploadMetadata."""

    def setUp(self):
        super().setUp()
        self.user = baker.make(settings.AUTH_USER_MODEL, email=fake.email())
        self.sql_upload_metadata = baker.make(SQLUploadMetadata)

    def test_default_str(self):
        assert str(self.sql_upload_metadata) == str(
            self.sql_upload_metadata.name
        )

    def test_is_complete_false(self):
        self.sql_upload_metadata.finish_time = None
        assert not self.sql_upload_metadata.is_complete

    def test_is_complete_true(self):
        self.sql_upload_metadata.finish_time = datetime.now()
        assert self.sql_upload_metadata.is_complete

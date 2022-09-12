import pytest
from faker import Faker
from model_bakery import baker
from rest_framework.test import APITestCase

from apps.common.tests.test_common import LoggedInMixin
from apps.sql_data.models import (
    DataSourceVersion,
    SQLDatabaseSource,
    SQLUploadChunk,
    SQLUploadMetadata,
    sql_extracts_upload_to,
)

pytestmark = pytest.mark.django_db

fake = Faker()


class TestDataSourceVersion(LoggedInMixin, APITestCase):
    """Test model: DataSourceVersion"""

    def setUp(self):
        super().setUp()
        self.data_source = baker.make(SQLDatabaseSource)
        self.data_source_version = baker.make(DataSourceVersion)

    def test_datasource_version_str(self):
        assert (
                str(self.data_source_version)
                == str(self.data_source_version.data_source)
                + " v("
                + str(self.data_source_version.data_source_version)
                + ")"
        )


class TestSQLUploadChunk(LoggedInMixin, APITestCase):
    """Test model: SQLUploadChunk"""

    def setUp(self):
        super().setUp()
        self.sql_upload_chunk = baker.make(SQLUploadChunk)

    def test_upload_chunk_name(self):
        assert str(self.sql_upload_chunk) == \
               str("%d__%s" % (self.sql_upload_chunk.chunk_index, str(self.sql_upload_chunk.pk)))

    def test_chunk_upload_path(self):
        upload_meta: SQLUploadMetadata = self.sql_upload_chunk.upload_metadata
        assert sql_extracts_upload_to(self.sql_upload_chunk, fake.text()) == "%s/%d__%s" % (
            upload_meta.upload_data_dir,
            self.sql_upload_chunk.chunk_index,
            self.sql_upload_chunk.pk,
        )


class TestSQLUploadMetadata(LoggedInMixin, APITestCase):
    """Test model: SQLUploadMetadata"""

    def setUp(self):
        super().setUp()
        self.sql_upload_metadata = baker.make(SQLUploadMetadata)

    def test_data_source_name(self):
        assert str(self.sql_upload_metadata.data_source_name) == \
               str(self.sql_upload_metadata.extract_metadata.data_source.name)

    def test_upload_completion(self):
        assert str(self.sql_upload_metadata.mark_as_complete(self.user)) == "None"

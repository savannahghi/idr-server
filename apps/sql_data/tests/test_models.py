from datetime import datetime

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
        data_source = self.data_source_version.data_source
        version = self.data_source_version.data_source_version
        assert str(self.data_source_version) == "%s v(%s)" % (
            str(data_source),
            version,
        )


class TestSQLUploadChunk(LoggedInMixin, APITestCase):
    """Test model: SQLUploadChunk"""

    def setUp(self):
        super().setUp()
        self.sql_upload_chunk = baker.make(SQLUploadChunk)

    def test_upload_chunk_name(self):
        index = self.sql_upload_chunk.chunk_index
        pk = self.sql_upload_chunk.pk
        assert str(self.sql_upload_chunk) == "{}__{}".format(index, pk)

    def test_chunk_upload_path(self):
        upload_meta: SQLUploadMetadata = self.sql_upload_chunk.upload_metadata
        upload_dir = upload_meta.upload_data_dir
        upload_extracts = sql_extracts_upload_to(
            self.sql_upload_chunk, fake.text()
        )
        index = self.sql_upload_chunk.chunk_index
        pk = self.sql_upload_chunk.pk
        assert str(upload_extracts) == "%s/%d__%s" % (
            str(upload_dir),
            index,
            str(pk),
        )


class TestSQLUploadMetadata(LoggedInMixin, APITestCase):
    """Test model: SQLUploadMetadata"""

    def setUp(self):
        super().setUp()
        self.sql_upload_metadata = baker.make(SQLUploadMetadata)

    def test_data_source_name(self):
        data_source = self.sql_upload_metadata.data_source_name
        data_source_name = (
            self.sql_upload_metadata.extract_metadata.data_source.name
        )
        assert str(data_source) == str(data_source_name)

    def test_upload_completion(self):
        self.sql_upload_metadata.mark_as_complete(self.user)
        assert self.sql_upload_metadata.updated_by == self.user
        assert (
            self.sql_upload_metadata.finish_time.date()
            == datetime.now().date()
        )

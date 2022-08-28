import pytest
from faker import Faker
from model_bakery import baker
from rest_framework.test import APITestCase

from apps.common.tests.test_common import LoggedInMixin
from apps.sql_data.models import (
    DataSourceVersion,
    SQLExtractMetadata,
    SQLUploadChunk,
    SQLUploadMetadata,
    sql_extracts_upload_to,
)

pytestmark = pytest.mark.django_db

fake = Faker()


class InitializeTestData(LoggedInMixin, APITestCase):
    def setUp(self):
        self.data_source_version = baker.make(DataSourceVersion)
        self.extract_metadata = baker.make(SQLExtractMetadata)
        self.sql_upload_metadata = baker.make(
            SQLUploadMetadata, extract_metadata=self.extract_metadata
        )
        self.upload_chunk = baker.make(
            SQLUploadChunk,
            upload_metadata=self.sql_upload_metadata,
            chunk_content=fake.file_name(),
        )

        super().setUp()

    def test_upload_metadata(self):
        assert (
            self.extract_metadata.data_source.name
            == self.sql_upload_metadata.data_source_name
        )
        assert (
            self.sql_upload_metadata.chunks_count
            == self.upload_chunk.upload_metadata.chunks_count
        )
        assert self.sql_upload_metadata.mark_as_complete(
            user=self.user
        ) == self.upload_chunk.upload_metadata.mark_as_complete(user=self.user)
        assert self.sql_upload_metadata.is_complete
        assert str(self.sql_upload_metadata.name) == str(
            self.sql_upload_metadata
        )

    def test_uploaded_chunk_str(self):
        assert str(self.upload_chunk) == str(
            self.upload_chunk.chunk_index
        ) + "__" + str(self.upload_chunk.id)

        sql_upload_chunk = self.upload_chunk
        chunk_index = sql_upload_chunk.chunk_index
        pk = str(sql_upload_chunk.pk)
        assert sql_extracts_upload_to(
            sql_upload_chunk, fake.text()
        ) == "%s/%d__%s" % (
            sql_upload_chunk.upload_metadata.upload_data_dir,
            chunk_index,
            pk,
        )

    def test_data_source_version_str(self):
        assert (
            str(self.data_source_version)
            == str(self.data_source_version.data_source)
            + " v("
            + str(self.data_source_version.data_source_version)
            + ")"
        )

    def test_sql_extract_metadata_str(self):
        assert str(self.extract_metadata.name) == str(self.extract_metadata)

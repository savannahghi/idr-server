import pytest
from faker import Faker
from model_bakery import baker
from rest_framework.test import APITestCase
from django.conf import settings

from apps.sql_data.models import SQLUploadMetadata, SQLExtractMetadata, \
    SQLUploadChunk, DataSourceVersion, sql_extracts_upload_to
from apps.tests.test_api import LoggedInMixin

pytestmark = pytest.mark.django_db

fake = Faker()


class InitializeTestData(LoggedInMixin, APITestCase):
    def setUp(self):
        self.upload_chunk = baker.make(SQLUploadChunk, chunk_content=fake.file_name())
        self.data_source_version = baker.make(DataSourceVersion)
        self.extract_metadata = baker.make(SQLExtractMetadata)
        self.sql_upload_metadata = baker.make(SQLUploadMetadata, extract_metadata=self.extract_metadata)

        super().setUp()

    def test_upload_metadata(self):
        assert self.extract_metadata.data_source.name == self.sql_upload_metadata.data_source_name

    def test_uploaded_chunk_str(self):
        assert str(self.upload_chunk) == str(self.upload_chunk.chunk_index) + "__" + str(self.upload_chunk.id)

        sql_upload_chunk = self.upload_chunk
        meta = sql_upload_chunk.upload_metadata.extract_metadata
        extracts_group_name: str = (
                meta.preferred_uploads_name or meta.name
        )
        name = sql_upload_chunk.upload_metadata.name
        chunk_index = sql_upload_chunk.chunk_index
        pk = str(sql_upload_chunk.pk)
        assert sql_extracts_upload_to(sql_upload_chunk, fake.text()) == "%s/%s/%s/%s/%d__%s" % (
            settings.BASE_EXTRACTS_UPLOAD_DIR_NAME,
            settings.SQL_EXTRACTS_UPLOAD_DIR_NAME,
            extracts_group_name, name, chunk_index, pk)

    def test_data_source_version_str(self):
        assert str(self.data_source_version) == str(self.data_source_version.data_source) + \
               " v(" + str(self.data_source_version.data_source_version) + ")"

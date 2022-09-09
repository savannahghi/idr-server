import pytest
from django.contrib.admin.sites import AdminSite
from faker import Faker
from model_bakery import baker
from rest_framework.test import APIRequestFactory, APITestCase

from apps.common.tests.test_common import LoggedInMixin
from apps.sql_data.admin import DataSourceVersionAdmin
from apps.sql_data.models import DataSourceVersion, SQLDatabaseSource

pytestmark = pytest.mark.django_db

fake = Faker()


class TestCoreModels(LoggedInMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.data_source_version = baker.make(DataSourceVersion)
        self.sql_data_source = baker.make(SQLDatabaseSource)

    def test_audit_base_model_audit_field_set_property(self):
        admin = DataSourceVersionAdmin(
            model=DataSourceVersion, admin_site=AdminSite()
        )
        return admin.audit_details_fieldset

    def test_save_model(self):
        data_source_admin = DataSourceVersionAdmin(
            model=DataSourceVersion, admin_site=AdminSite()
        )
        request = self.factory.request()
        request.user = self.user
        data_source_admin.save_model(
            obj=self.data_source_version,
            request=request,
            form=None,
            change=None,
        )

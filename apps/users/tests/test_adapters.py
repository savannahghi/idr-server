import pytest
from faker import Faker
from rest_framework.test import APIRequestFactory, APITestCase

from apps.common.tests.test_common import LoggedInMixin
from apps.users.adapters import AccountAdapter, SocialAccountAdapter

pytestmark = pytest.mark.django_db

fake = Faker()


class TestAdapters(LoggedInMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()

    def test_account_adapter(self):
        request = self.factory.request()
        request.user = self.user
        response = AccountAdapter.is_open_for_signup(self, request)
        assert response is True

    def test_social_account_adapter(self):
        request = self.factory.request()
        request.user = self.user
        response = SocialAccountAdapter.is_open_for_signup(
            self, request, sociallogin=None
        )
        assert response is True

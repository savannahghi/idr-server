from unittest import TestCase

from apps.common.tests.test_common import LoggedInMixin
from apps.frontend.views import HomeView


class TestViews(LoggedInMixin, TestCase):
    def test_home_view_context(self):
        view = HomeView()
        view.get_context_data()

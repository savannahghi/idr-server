from django.urls import path
from knox.views import LogoutAllView, LogoutView

from .apiviews import LoginView

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="api_login"),
    path("auth/logout/", LogoutView.as_view(), name="api_logout"),
    path("auth/logoutall/", LogoutAllView.as_view(), name="api_logoutall"),
]

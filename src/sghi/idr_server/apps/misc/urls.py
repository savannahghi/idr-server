from django.urls import path

from .views import trigger_error

app_name = "misc"
urlpatterns = [path("sentry_debug/", trigger_error, name="sentry_debug")]

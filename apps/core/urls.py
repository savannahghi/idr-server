from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .apiviews import GenericSourceViewSet


router = DefaultRouter()
router.register("generic_sources", GenericSourceViewSet)



urlpatterns = [
    path("", include(router.urls))
]

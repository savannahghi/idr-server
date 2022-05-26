from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .apiviews import SimpleMetadataViewSet, SourceVersionViewSet


router = DefaultRouter()
router.register("simple_sql_metadata", SimpleMetadataViewSet)
router.register("source_versions", SourceVersionViewSet)


urlpatterns = [
    path("", include(router.urls))
]

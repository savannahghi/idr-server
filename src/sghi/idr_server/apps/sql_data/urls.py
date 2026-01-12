from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apiviews import (
    DataSourceVersionViewSet,
    SQLDatabaseViewSet,
    SQLExtractMetadataViewSet,
    SQLUploadChunkViewSet,
    SQLUploadMetadataViewSet,
)

router = DefaultRouter()
router.register("data_source_versions", DataSourceVersionViewSet)
router.register("sql_database_sources", SQLDatabaseViewSet)
router.register("sql_extract_metadata", SQLExtractMetadataViewSet)
router.register("sql_upload_chunks", SQLUploadChunkViewSet)
router.register("sql_upload_metadata", SQLUploadMetadataViewSet)


urlpatterns = [path("sql_data/", include(router.urls))]

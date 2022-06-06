from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apiviews import DashboardViewSet, VisualizationViewSet

router = DefaultRouter()
router.register("dashboards", DashboardViewSet)
router.register("visualizations", VisualizationViewSet)


urlpatterns = [path("dashboards/", include(router.urls))]

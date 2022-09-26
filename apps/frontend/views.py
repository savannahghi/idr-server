from typing import Any, Dict

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.dashboards.models import Dashboard


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "pages/frontend/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data()
        context["GOOGLE_ANALYTICS_ID"] = settings.GOOGLE_ANALYTICS_ID
        Dashboard.objects.all()
        return context

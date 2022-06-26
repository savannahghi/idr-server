from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.dashboards.models import Dashboard


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "pages/frontend/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data()
        Dashboard.objects.all()
        return context

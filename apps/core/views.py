from django.views.generic.base import View
from django.shortcuts import render
 
class HomeView(View):
    def get(self, request):
        return render(request, "templates/dashboards.html")

"""idr_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import RedirectView

from apps.frontend.views import HomeView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("api/", include("apps.app_auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("api/", include("apps.core.urls")),
    path("api/", include("apps.sql_sources.urls")),
    path("misc/", include("apps.misc.urls")),
    path("ui/", include("apps.frontend.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
    re_path(
        r"^favicon\.ico$",
        RedirectView.as_view(
            url=settings.STATIC_URL + "favicon.ico",
            permanent=True
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()
    if settings.DEBUG:
        # This allows the error pages to be debugged during development, just visit
        # these url in browser to see how these error pages look like.
        urlpatterns += [
            path(
                "400/",
                default_views.bad_request,
                kwargs={"exception": Exception("Bad Request!")},
            ),
            path(
                "403/",
                default_views.permission_denied,
                kwargs={"exception": Exception("Permission Denied")},
            ),
            path(
                "404/",
                default_views.page_not_found,
                kwargs={"exception": Exception("Page not Found")},
            ),
            path("500/", default_views.server_error),
        ]

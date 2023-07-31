"""PortfolioSite URL Configuration

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
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic.base import RedirectView
from Main.sitemaps import HomeSitemap, ProjectSitemap

sitemaps = {
    "home": HomeSitemap,
    "projects": ProjectSitemap,
}
SITEMAP_URL = "sitemap.xml/"

urlpatterns = [
    path("", include("Main.urls")),
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path(
        SITEMAP_URL,
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("sitemap.txt/", RedirectView.as_view(url="/" + SITEMAP_URL, permanent=False)),
    path("sitemap/", RedirectView.as_view(url="/" + SITEMAP_URL, permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# add debug toolbar urls if in DEBUG mode
if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))

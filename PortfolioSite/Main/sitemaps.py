from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from Main.models import Project

class ProjectSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.7
    
    def items(self):
        return Project.objects.filter(published=True)
    
    def lastmod(self, obj):
        return obj.last_modified

class HomeSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)

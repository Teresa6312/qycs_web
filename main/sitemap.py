from django.contrib.sitemaps import Sitemap
from .models import CollectionPoint, Resource


from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['collection_points', 'shopping']

    def location(self, item):
        return reverse(item)


class CollectionPointSitemap(Sitemap):
    def items(self):
        return CollectionPoint.objects.all()

class ResourceSitemap(Sitemap):
    def items(self):
        return Resource.objects.all()

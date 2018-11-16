from django.contrib.sitemaps import Sitemap
from .models import CollectionPoint


from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'collection_points', 'shopping', 'price_list']

    def location(self, item):
        return reverse(item)


class CollectionPointSitemap(Sitemap):
    def items(self):
        return CollectionPoint.objects.all()

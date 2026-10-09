from django.contrib.sitemaps import Sitemap
from .models import Product

class ShopSitemap(Sitemap):
    priority = 0.5
    changefreq = 'never'

    def items(self):
        return Product.objects.filter(archived=False).order_by("pk")

    def lastmod(self, obj: Product):
        return obj.created_at

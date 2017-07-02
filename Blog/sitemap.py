from django.contrib.sitemaps import Sitemap
from Blog.models import Blog


class BlogpostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.created
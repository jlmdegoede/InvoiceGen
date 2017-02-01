from django.conf.urls import include, url
from django.contrib import admin
import Orders.views
import Agreements.views
import Invoices.views
import Companies.views
import Settings.views
import Todo.views
import HourRegistration.views
import Statistics.views
import Mail.views
from django.conf import settings
from django.conf.urls.static import static
import django.contrib.auth.views
from django.contrib.auth.decorators import login_required, permission_required
import Tenants.views
from tenant_schemas.utils import get_public_schema_name
from Blog.sitemap import BlogpostSitemap
from django.views.generic import TemplateView
import Blog.views
import PaymentProcessor.views
from django.contrib.sitemaps import views

sitemaps = {
    'blogs': BlogpostSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Tenants.views.index, name='index'),
    #url(r'^registreren/$', Customer.views.CreateNewInvoiceSite.as_view()),
    url(r'^inloggen/$', Tenants.views.MyDataView.as_view()),
    url(r'^get-subscription-status/$', Tenants.views.get_subscription_status),
    url(r'^contact/$', TemplateView.as_view(template_name='Tenants/contact.html')),
    url(r'^status/$', TemplateView.as_view(template_name='Tenants/status.html')),
    url(r'^functies/$', TemplateView.as_view(template_name='Tenants/functions.html')),
    #url(r'^wunderlist/$', Todo.views.index),
    #url(r'^wunderlist-code/$', Todo.views.get_code),
    url(r'^blog/$', Blog.views.index),
    url(r'^blog/(?P<blog_id>\d+)/(?P<slug>.+)/$', Blog.views.view_blogpost, name='view_blogpost'),
    url(r'^sitemap\.xml$', views.index, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', views.sitemap, {'sitemaps': sitemaps}),
    url(r'^betaling/start/$', PaymentProcessor.views.start_mollie_payment),
    url(r'^betaling/status/$', PaymentProcessor.views.status_change_mollie_payment),
    url(r'^betaling/succes$', PaymentProcessor.views.complete_change_mollie_payment),
    url(r'^tenants/$', Tenants.views.create_public_tenant, name='tenants'),
]

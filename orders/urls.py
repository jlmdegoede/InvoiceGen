from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
import orders.views

urlpatterns = [
    url(r'^(?P<product_id>\d+)/(.*)$', orders.views.view_product, name='view_product'),
    url(r'^toevoegen/$', orders.views.add_product, name='add_product'),
    url(r'^wijzigen/(?P<product_id>\d+)/$', permission_required('orders.change_product')(orders.views.EditProductView.as_view()), name='edit_product'),
    url(r'^verwijderen/(?P<product_id>\d+)/$', orders.views.delete_product, name='delete_product'),
    url(r'^verwijder/bijlage/$', orders.views.attachment_delete, name='delete_product_attachment'),
    url(r'^afronden/$', orders.views.mark_products_as_done, name='mark_products_as_done'),
    url(r'^list-hourregistration/$', orders.views.get_list_of_orders_hourregistration, name='get_list_of_orders_hourregistration'),
    url(r'^jaar/(?P<year>\d+)/$', orders.views.view_products_in_year, name='view_products_in_year'),

]


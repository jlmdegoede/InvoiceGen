from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
import Orders.views

urlpatterns = [
    url(r'^(?P<product_id>\d+)/(.*)$', Orders.views.view_product, name='view_product'),
    url(r'^toevoegen/$', Orders.views.add_product, name='add_product'),
    url(r'^wijzigen/(?P<product_id>\d+)/$', permission_required('Orders.change_product')(Orders.views.EditProductView.as_view()), name='edit_product'),
    url(r'^verwijderen/(?P<product_id>\d+)/$', Orders.views.delete_product, name='delete_product'),
    url(r'^afronden/$', Orders.views.mark_products_as_done, name='mark_products_as_done'),
    url(r'^list-hourregistration/$', Orders.views.get_list_of_orders_hourregistration, name='get_list_of_orders_hourregistration'),
    url(r'^jaar/(?P<year>\d+)/$', Orders.views.view_products_in_year, name='view_products_in_year'),

]


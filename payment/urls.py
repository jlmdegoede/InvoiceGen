from django.conf.urls import url

import payment.views

urlpatterns = [
    url(r'^mollie/(?P<invoice_id>\d+)$', payment.views.mollie_payment, name='mollie_payment'),
    url(r'^bunq/(?P<invoice_id>\d+)$', payment.views.bunq_request, name='bunq_request'),

]


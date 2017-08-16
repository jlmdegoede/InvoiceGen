from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required

import invoices.views

urlpatterns = [
    url(r'^$', invoices.views.get_outgoing_invoices, name='get_invoices'),
    url(r'^generate/invoice/$', invoices.views.generate_invoice, name='generate_invoice'),
    url(r'^inkomend/$', invoices.views.get_incoming_invoices, name='get_incoming_invoices'),
    url(r'^toevoegen/$', permission_required('invoices.add_outgoinginvoice')(invoices.views.AddOutgoingInvoice.as_view()), name='add_outgoing_invoice'),
    url(r'^inkomend/toevoegen/$', invoices.views.add_incoming_invoice, name='add_incoming_invoice'),
    url(r'^wijzigen/(?P<invoice_id>\d+)/$', permission_required('invoices.change_outgoinginvoice')(invoices.views.EditOutgoingInvoice.as_view()), name='edit_outgoing_invoice'),
    url(r'^inkomend/wijzigen/(?P<invoice_id>\d+)/$', permission_required('invoices.change_incominginvoice')(invoices.views.EditIncomingInvoice.as_view()),
        name='edit_incoming_invoice'),
    url(r'^verwijderen/(?P<invoice_id>\d+)/$', invoices.views.delete_outgoing_invoice,
        name='delete_outgoing_invoice'),
    url(r'^inkomend/verwijderen/(?P<invoice_id>\d+)/$', invoices.views.delete_incoming_invoice,
        name='delete_incoming_invoice'),
    url(r'^inkomend/(?P<invoice_id>\d+)/$', invoices.views.detail_incoming_invoice,
        name='detail_incoming_invoice'),
    url(r'^uitgaand/(?P<invoice_id>\d+)/$', invoices.views.detail_outgoing_invoice,
        name='detail_outgoing_invoice'),
    url(r'^bekijken/(?P<invoice_url>\w+)/$', invoices.views.view_outgoing_invoice_guest,
        name='view_outgoing_invoice_guest'),
    url(r'^bekijken/(?P<invoice_url>\w+)/(?P<paid>\w+)$', invoices.views.view_outgoing_invoice_guest,
        name='view_outgoing_invoice_guest_paid'),
    url(r'^delen/(?P<invoice_id>\d+)/$', invoices.views.share_link_to_outgoing_invoice,
        name='share_link_to_outgoing_invoice'),
    url(r'^email/(?P<invoice_id>\d+)/$', login_required(invoices.views.SendOutgoingInvoicePerEmail.as_view()),
        name='email_outgoing_invoice'),
    url(r'^downloaden/(?P<file_type>\w+)/(?P<invoice_id>\d+)/$',
        invoices.views.download_latest_generated_invoice, name='download_invoice'),
    url(r'^status/(?P<task_id>.+)/$', invoices.views.check_pdf_task_status, name='check_pdf_task_status'),
    url(r'^genereren/(?P<invoice_id>\d+)/$', invoices.views.generate_pdf, name='generate_pdf'),

]

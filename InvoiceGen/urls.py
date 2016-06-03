from django.conf.urls import patterns, include, url
from django.contrib import admin
import Orders.views
import Agreements.views
import Invoices.views
import Companies.views
import Settings.views
# import RestApi.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Orders.views.index, name='index'),
    url(r'^accounts/login/$', Orders.views.user_login, name='user_login'),
    url(r'^logout/$', Orders.views.user_logout, name='logout'),
    url(r'^opdracht/(?P<articleid>\d+)/(.*)$', Orders.views.view_article, name='view_article'),
    url(r'^opdracht/toevoegen/$', Orders.views.add_article, name='add_article'),
    url(r'^opdracht/wijzigen/(?P<articleid>\d+)/$', Orders.views.edit_article, name='edit_article'),
    url(r'^opdracht/verwijderen/(?P<articleid>\d+)/$', Orders.views.delete_article, name='delete_article'),
    url(r'^generate/invoice/$', Invoices.views.generate_invoice, name='generate_invoice'),
    url(r'^facturen/$', Invoices.views.get_invoices, name='get_invoices'),
    url(r'^facturen/toevoegen/$', Invoices.views.add_invoice, name='add_invoice'),
    url(r'^facturen/wijzigen/(?P<invoiceid>\d+)/$', Invoices.views.edit_invoice, name='edit_invoice'),
    url(r'^facturen/verwijderen/(?P<invoiceid>\d+)/$', Invoices.views.delete_invoice, name='delete_invoice'),
    url(r'^markdown/(?P<invoice_id>\d+)/', Orders.views.view_markdown, name='view_markdown'),
    url(r'^download/md/(?P<invoice_id>\d+)/', Orders.views.download_markdown, name='download_markdown'),

    url(r'^instellingen/$', Settings.views.settings, name='settings'),
    url(r'^instellingen/kleuren/$', Settings.views.set_colors, name='set_colors'),
    url(r'^instellingen/reset-kleuren/$', Settings.views.reset_colors, name='reset_colors'),

    url(r'^statistieken/$', Orders.views.view_statistics, name='statistics'),

    url(r'^opdrachtgevers/$', Companies.views.index, name='company_index'),
    url(r'^opdrachtgevers/nieuw$', Companies.views.add_company, name='company_add'),
    url(r'^opdrachtgevers/wijzigen/(?P<company_id>\d+)/$', Companies.views.edit_company, name='company_edit'),
    url(r'^opdrachtgevers/verwijderen/(?P<company_id>\d+)/$', Companies.views.delete_company, name='company_delete'),
    url(r'^client/add/inline/$', Orders.views.add_company_inline, name='add_company_inline'),

    url(r'^overeenkomsten/$', Agreements.views.agreement_index,
        name='agreement_index'),
    url(r'^overeenkomsten/nieuwe-modelovereenkomst/$', Agreements.views.add_agreement_text,
        name='add_agreement_text'),
    url(r'^overeenkomsten/nieuw/$', Agreements.views.add_agreement,
        name='add_agreement'),
    url(r'^overeenkomsten/ondertekenen/(?P<url>\w+)$', Agreements.views.view_agreement,
        name='view_agreement'),
    url(r'^overeenkomsten/verwijderen/(?P<agreement_id>\d+)/$', Agreements.views.delete_agreement,
        name='delete_agreement'),
    url(r'^overeenkomsten/modelovereenkomsten/$', Agreements.views.index_model_agreements,
        name='index_model_agreements'),
    url(r'^overeenkomsten/modelovereenkomsten-bewerken/(?P<model_agreement_id>\d+)/$', Agreements.views.edit_model_agreement,
        name='edit_model_agreement'),
]

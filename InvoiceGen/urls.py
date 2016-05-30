from django.conf.urls import patterns, include, url
from django.contrib import admin
import FactuurMaker.views
import AgreementModule.views
import Invoices.views
# import RestApi.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', FactuurMaker.views.index, name='index'),
    url(r'^accounts/login/$', FactuurMaker.views.user_login, name='user_login'),
    url(r'^logout/$', FactuurMaker.views.user_logout, name='logout'),
    url(r'^opdracht/(?P<articleid>\d+)/(.*)$', FactuurMaker.views.view_article, name='view_article'),
    url(r'^opdracht/toevoegen/$', FactuurMaker.views.add_article, name='add_article'),
    url(r'^opdracht/wijzigen/(?P<articleid>\d+)/$', FactuurMaker.views.edit_article, name='edit_article'),
    url(r'^opdracht/verwijderen/(?P<articleid>\d+)/$', FactuurMaker.views.delete_article, name='delete_article'),
    url(r'^generate/invoice/$', Invoices.views.generate_invoice, name='generate_invoice'),
    url(r'^facturen/$', Invoices.views.get_invoices, name='get_invoices'),
    url(r'^facturen/toevoegen/$', Invoices.views.add_invoice, name='add_invoice'),
    url(r'^facturen/wijzigen/(?P<invoiceid>\d+)/$', Invoices.views.edit_invoice, name='edit_invoice'),
    url(r'^facturen/verwijderen/(?P<invoiceid>\d+)/$', Invoices.views.delete_invoice, name='delete_invoice'),
    url(r'^markdown/(?P<invoice_id>\d+)/', FactuurMaker.views.view_markdown, name='view_markdown'),
    url(r'^download/md/(?P<invoice_id>\d+)/', FactuurMaker.views.download_markdown, name='download_markdown'),
    url(r'^instellingen/$', FactuurMaker.views.settings, name='settings'),
    url(r'^instellingen/gebruiker/(?P<userid>\d+)/company/(?P<companyid>\d+)$', FactuurMaker.views.settings, name='settings'),
    url(r'^statistieken/$', FactuurMaker.views.view_statistics, name='statistics'),
    url(r'^client/add/inline/$', FactuurMaker.views.add_company_inline, name='add_company_inline'),

    url(r'^overeenkomsten/$', AgreementModule.views.agreement_index,
        name='agreement_index'),
    url(r'^overeenkomsten/nieuwe-modelovereenkomst/$', AgreementModule.views.add_agreement_text,
        name='add_agreement_text'),
    url(r'^overeenkomsten/nieuw/$', AgreementModule.views.add_agreement,
        name='add_agreement'),
    url(r'^overeenkomsten/ondertekenen/(?P<url>\w+)$', AgreementModule.views.view_agreement,
        name='view_agreement'),
    url(r'^overeenkomsten/verwijderen/(?P<agreement_id>\d+)/$', AgreementModule.views.delete_agreement,
        name='delete_agreement'),
]

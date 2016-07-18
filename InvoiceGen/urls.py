from django.conf.urls import patterns, include, url
from django.contrib import admin
import Orders.views
import Agreements.views
import Invoices.views
import Companies.views
import Settings.views
import Todo.views
import HourRegistration.views
from django.conf import settings
from django.conf.urls.static import static
import django.contrib.auth.views

urlpatterns = [
    url(r'^$', Orders.views.index, name='index'),
    url(r'^accounts/login/$', Orders.views.user_login, name='user_login'),
    url(r'^inloggen/via-website/$', Orders.views.user_login_placeholder_email, name='user_login_placeholder_email'),
    url(r'^logout/$', Orders.views.user_logout, name='logout'),

    url(r'^opdracht/(?P<productid>\d+)/(.*)$', Orders.views.view_product, name='view_product'),
    url(r'^opdracht/toevoegen/$', Orders.views.add_article, name='add_product'),
    url(r'^opdracht/wijzigen/(?P<articleid>\d+)/$', Orders.views.edit_article, name='edit_product'),
    url(r'^opdracht/verwijderen/(?P<articleid>\d+)/$', Orders.views.delete_article, name='delete_product'),
    url(r'^opdracht/afronden/$', Orders.views.mark_products_as_done, name='mark_products_as_done'),
    url(r'^opdracht/list-hourregistration/$', Orders.views.get_list_of_orders_hourregistration, name='get_list_of_orders_hourregistration'),

    url(r'^generate/invoice/$', Invoices.views.generate_invoice, name='generate_invoice'),
    url(r'^facturen/$', Invoices.views.get_outgoing_invoices, name='get_invoices'),
    url(r'^facturen/inkomend/$', Invoices.views.get_incoming_invoices, name='get_incoming_invoices'),
    url(r'^facturen/toevoegen/$', Invoices.views.add_outgoing_invoice, name='add_outgoing_invoice'),
    url(r'^facturen/inkomend/toevoegen/$', Invoices.views.add_incoming_invoice, name='add_incoming_invoice'),
    url(r'^facturen/wijzigen/(?P<invoiceid>\d+)/$', Invoices.views.edit_outgoing_invoice, name='edit_outgoing_invoice'),
    url(r'^facturen/inkomend/wijzigen/(?P<invoiceid>\d+)/$', Invoices.views.edit_incoming_invoice, name='edit_incoming_invoice'),
    url(r'^facturen/verwijderen/(?P<invoiceid>\d+)/$', Invoices.views.delete_outgoing_invoice, name='delete_outgoing_invoice'),
    url(r'^facturen/inkomend/verwijderen/(?P<invoiceid>\d+)/$', Invoices.views.delete_incoming_invoice, name='delete_incoming_invoice'),
    url(r'^factuur/inkomend/(?P<invoice_id>\d+)/$', Invoices.views.detail_incoming_invoice, name='detail_incoming_invoice'),
    url(r'^factuur/uitgaand/(?P<invoice_id>\d+)/$', Invoices.views.detail_outgoing_invoice, name='detail_outgoing_invoice'),
    url(r'^pdf/(?P<invoice_id>\d+)/$', Invoices.views.get_invoice_pdf, name='download_pdf'),
    url(r'^docx/(?P<invoice_id>\d+)/$', Invoices.views.get_invoice_docx, name='download_docx'),
    url(r'^md/(?P<invoice_id>\d+)/$', Invoices.views.get_invoice_markdown, name='download_markdown'),

    url(r'^instellingen/$', Settings.views.settings, name='settings'),
    url(r'^instellingen/kleuren/$', Settings.views.set_colors, name='set_colors'),
    url(r'^instellingen/reset-kleuren/$', Settings.views.reset_colors, name='reset_colors'),

    url(r'^statistieken/$', Orders.views.view_statistics, name='statistics'),

    url(r'^opdrachtgevers/$', Companies.views.index, name='company_index'),
    url(r'^opdrachtgevers/nieuw$', Companies.views.add_company, name='company_add'),
    url(r'^opdrachtgevers/wijzigen/(?P<company_id>\d+)/$', Companies.views.edit_company, name='company_edit'),
    url(r'^opdrachtgevers/verwijderen/(?P<company_id>\d+)/$', Companies.views.delete_company, name='company_delete'),
    url(r'^client/add/inline/$', Orders.views.add_company_inline, name='add_company_inline'),

    url(r'^zoeken/$', Orders.views.search, name='search'),

    url(r'^urenregistratie/start/(?P<product_id>\d+)/$', HourRegistration.views.start_time_tracking, name='start_time_tracking'),
    url(r'^urenregistratie/stop/(?P<product_id>\d+)/$', HourRegistration.views.end_time_tracking, name='end_time_tracking'),
    url(r'^urenregistratie/bestaand/$', HourRegistration.views.existing_time_tracking, name='existing_time_tracking'),
    url(r'^urenregistratie/eindtijd/$', HourRegistration.views.set_end_time, name='set_end_time'),
    url(r'^urenregistratie/nieuw/$', HourRegistration.views.create_new_hour_registration, name='create_new_hour_registration'),

    url(r'^overeenkomsten/$', Agreements.views.agreement_index,
        name='agreement_index'),
    url(r'^overeenkomsten/modelovereenkomsten/nieuw/$', Agreements.views.add_agreement_text,
        name='add_agreement_text'),
    url(r'^overeenkomsten/nieuw/$', Agreements.views.add_agreement,
        name='add_agreement'),
    url(r'^overeenkomsten/ondertekenen/(?P<url>\w+)/$', Agreements.views.view_agreement,
        name='view_agreement'),
    url(r'^overeenkomsten/ondertekenen/contractor/(?P<url>\w+)/$', Agreements.views.sign_agreement_contractor,
      name='sign_contractor'),
    url(r'^overeenkomsten/ondertekenen/client/(?P<url>\w+)/$', Agreements.views.sign_agreement_client,
      name='sign_client'),
    url(r'^overeenkomsten/verwijderen/(?P<agreement_id>\d+)/$', Agreements.views.delete_agreement,
        name='delete_agreement'),
    url(r'^overeenkomsten/modelovereenkomsten/$', Agreements.views.index_model_agreements,
        name='index_model_agreements'),
    url(r'^overeenkomsten/modelovereenkomsten/bewerken/(?P<model_agreement_id>\d+)/$', Agreements.views.edit_model_agreement,
        name='edit_model_agreement'),
    url(r'^overeenkomsten/modelovereenkomsten/verwijderen/(?P<model_agreement_text_id>\d+)/$',
        Agreements.views.delete_model_agreement,
        name='delete_model_agreement'),

      url(r'^wachtwoord-vergeten/$', django.contrib.auth.views.password_reset, {'post_reset_redirect': '/wachtwoord-vergeten/klaar/'},
          name="password_reset"),
      url(r'^wachtwoord-vergeten/klaar/$',
       django.contrib.auth.views.password_reset_done),
      url(r'^wachtwoord-vergeten/instellen/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
       django.contrib.auth.views.password_reset_confirm,
       {'post_reset_redirect': '/wachtwoord-vergeten/opnieuw-ingesteld/'},
          name="password_reset_confirm"),
      url(r'^wachtwoord-vergeten/opnieuw-ingesteld/$',
       django.contrib.auth.views.password_reset_complete),

    url(r'^wunderlist-auth/$', Todo.views.save_auth_token, name='save_auth_token'),
    url(r'^wunderlist-nieuwe-taak/$', Todo.views.create_task_from_order, name='create_new_task'),
    url(r'^wunderlist-instellingen/$', Settings.views.save_wunderlist_settings, name='save_wunderlist_settings'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

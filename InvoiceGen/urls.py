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
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', Orders.views.index, name='index'),
    url(r'^accounts/login/$', Orders.views.user_login, name='user_login'),
    url(r'^inloggen/via-website/$', Orders.views.user_login_placeholder_email, name='user_login_placeholder_email'),
    url(r'^logout/$', Orders.views.user_logout, name='logout'),

    url(r'^opdracht/(?P<product_id>\d+)/(.*)$', Orders.views.view_product, name='view_product'),
    url(r'^opdracht/toevoegen/$', Orders.views.add_product, name='add_product'),
    url(r'^opdracht/wijzigen/(?P<product_id>\d+)/$', Orders.views.edit_product, name='edit_product'),
    url(r'^opdracht/verwijderen/(?P<product_id>\d+)/$', Orders.views.delete_product, name='delete_product'),
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
    url(r'^factuur/bekijken/(?P<invoice_url>\w+)/$', Invoices.views.view_outgoing_invoice_guest, name='view_outgoing_invoice_guest'),
    url(r'^factuur/delen/(?P<invoice_id>\d+)/$', Invoices.views.share_link_to_outgoing_invoice, name='share_link_to_outgoing_invoice'),
    url(r'^factuur/email/(?P<invoice_id>\d+)/$', login_required(Invoices.views.SendOutgoingInvoicePerEmail.as_view()), name='email_outgoing_invoice'),
    url(r'^factuur/downloaden/(?P<file_type>\w+)/(?P<invoice_id>\d+)/$', Invoices.views.download_latest_generated_invoice, name='download_invoice'),

    url(r'^email/templates/$', Mail.views.list_view_templates, name='list_view_templates'),
    url(r'^email/templates/nieuw/$', Mail.views.NewEditEmailTemplate.as_view(), name='new_email_template'),
    url(r'^email/templates/bewerken/(?P<email_template_id>\d+)/$', Mail.views.NewEditEmailTemplate.as_view(), name='edit_email_template'),
    url(r'^email/templates/verwijderen/$', Mail.views.delete_email_template, name='delete_email_template'),
    url(r'^email/verzonden/$', login_required(Mail.views.SentEmailListView.as_view()), name='sent_email_list'),
    url(r'^email/verzenden/$', Mail.views.save_and_send_email, name='save_and_send_email'),
    url(r'^email/inhoud/$', Mail.views.get_email_contents, name='get_email_contents'),
    url(r'^email/get-template/$', Mail.views.get_template, name='get_template'),

    url(r'^instellingen/$', Settings.views.settings, name='settings'),
    url(r'^instellingen/verlengen/$', Settings.views.renew_subscription, name='renew_subscription'),
    url(r'^instellingen/nieuwe-gebruiker$', Settings.views.create_new_user, name='create_new_user'),
    url(r'^instellingen/gebruiker/bewerken/(?P<user_id>\d+)/$', Settings.views.EditUserView.as_view(), name='edit_user'),

    url(r'^statistieken/$', Statistics.views.view_statistics, name='statistics'),

    url(r'^statistieken/btw-aangifte$', Statistics.views.view_btw_aangifte, name='btw_aangifte'),

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
    url(r'^urenregistratie/verwijderen/$', HourRegistration.views.delete_time_tracking, name='delete_time_tracking'),
    url(r'^urenregistratie/omschrijving/$', HourRegistration.views.add_description_to_hourregistration, name='add_description_to_hourregistration'),

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

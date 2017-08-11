import django.contrib.auth.views
from django import conf
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from markdownx import urls as markdownx
from rest_framework import routers

import agreements.views
import companies.views
import hour_registration.views
import mail.views
import orders.views
import settings.views
import statistics.views
from companies.views import CompanyViewSet
from invoices.views import OutgoingInvoiceViewSet
from orders.views import ProductViewSet


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'outgoing-invoices', OutgoingInvoiceViewSet)

urlpatterns = [

                  url(r'^$', orders.views.index, name='index'),
                  url(r'^accounts/login/$', orders.views.user_login, name='user_login'),
                  url(r'^logout/$', orders.views.user_logout, name='logout'),
                  url(r'^zoeken/$', orders.views.search, name='search'),
                  url(r'^admin/', admin.site.urls),

                  url(r'^opdracht/', include('orders.urls')),
                  url(r'^facturen/', include('invoices.urls')),

                  url(r'^email/templates/$', mail.views.list_view_templates, name='list_view_templates'),
                  url(r'^email/templates/nieuw/$', mail.views.NewEditEmailTemplate.as_view(),
                      name='new_email_template'),
                  url(r'^email/templates/bewerken/(?P<email_template_id>\d+)/$',
                      mail.views.NewEditEmailTemplate.as_view(), name='edit_email_template'),
                  url(r'^email/templates/verwijderen/$', mail.views.delete_email_template,
                      name='delete_email_template'),
                  url(r'^email/verzonden/$', login_required(mail.views.SentEmailListView.as_view()),
                      name='sent_email_list'),
                  url(r'^email/verzenden/$', mail.views.save_and_send_email, name='save_and_send_email'),
                  url(r'^email/inhoud/$', mail.views.get_email_contents, name='get_email_contents'),
                  url(r'^email/get-template/$', mail.views.get_template, name='get_template'),

                  url(r'^instellingen/$', settings.views.settings, name='settings'),
                  url(r'^instellingen/persoonlijk$', settings.views.PersonalSettings.as_view(),
                      name='personal_settings'),
                  url(r'^instellingen/nieuwe-gebruiker$', settings.views.UserSettings.as_view(),
                      name='create_new_user'),
                  url(r'^instellingen/gebruiker/bewerken/(?P<user_id>\d+)/$', settings.views.EditUserView.as_view(),
                      name='edit_user'),
                  url(r'^instellingen/gebruiker/verwijderen$', settings.views.delete_user, name='delete_user'),
                  url(r'^instellingen/factuursjabloon/standaard$', settings.views.save_default_invoice_template,
                      name='default_invoice'),

                  url(r'^statistieken/$', statistics.views.view_statistics, name='statistics'),

                  url(r'^statistieken/btw-aangifte$', statistics.views.view_btw_aangifte, name='btw_aangifte'),

                  url(r'^opdrachtgevers/$', companies.views.index, name='company_index'),
                  url(r'^opdrachtgevers/nieuw$', companies.views.add_company, name='company_add'),
                  url(r'^opdrachtgevers/wijzigen/(?P<company_id>\d+)/$', companies.views.edit_company,
                      name='company_edit'),
                  url(r'^opdrachtgevers/verwijderen/(?P<company_id>\d+)/$', companies.views.delete_company,
                      name='company_delete'),
                  url(r'^client/add/inline/$', orders.views.add_company_inline, name='add_company_inline'),
                  url(r'^client/default-price/(?P<company_id>\d+)$', companies.views.default_price_for_company,
                      name='company_price'),

                  url(r'^urenregistratie/start/(?P<product_id>\d+)/$', hour_registration.views.start_time_tracking,
                      name='start_time_tracking'),
                  url(r'^urenregistratie/stop/(?P<product_id>\d+)/$', hour_registration.views.end_time_tracking,
                      name='end_time_tracking'),
                  url(r'^urenregistratie/bestaand/$', hour_registration.views.existing_time_tracking,
                      name='existing_time_tracking'),
                  url(r'^urenregistratie/eindtijd/$', hour_registration.views.set_end_time, name='set_end_time'),
                  url(r'^urenregistratie/nieuw/$', hour_registration.views.create_new_hour_registration,
                      name='create_new_hour_registration'),
                  url(r'^urenregistratie/verwijderen/$', hour_registration.views.delete_time_tracking,
                      name='delete_time_tracking'),
                  url(r'^urenregistratie/omschrijving/$', hour_registration.views.add_description_to_hourregistration,
                      name='add_description_to_hourregistration'),

                  url(r'^overeenkomsten/$', agreements.views.agreement_index,
                      name='agreement_index'),
                  url(r'^overeenkomsten/modelovereenkomsten/nieuw/$', agreements.views.add_agreement_text,
                      name='add_agreement_text'),
                  url(r'^overeenkomsten/nieuw/$', agreements.views.add_agreement,
                      name='add_agreement'),
                  url(r'^overeenkomsten/ondertekenen/(?P<url>\w+)/$', agreements.views.view_agreement,
                      name='view_agreement'),
                  url(r'^overeenkomsten/ondertekenen/contractor/(?P<url>\w+)/$',
                      agreements.views.sign_agreement_contractor,
                      name='sign_contractor'),
                  url(r'^overeenkomsten/ondertekenen/client/(?P<url>\w+)/$', agreements.views.sign_agreement_client,
                      name='sign_client'),
                  url(r'^overeenkomsten/verwijderen/(?P<agreement_id>\d+)/$', agreements.views.delete_agreement,
                      name='delete_agreement'),
                  url(r'^overeenkomsten/modelovereenkomsten/$', agreements.views.index_model_agreements,
                      name='index_model_agreements'),
                  url(r'^overeenkomsten/modelovereenkomsten/bewerken/(?P<model_agreement_id>\d+)/$',
                      agreements.views.edit_model_agreement,
                      name='edit_model_agreement'),
                  url(r'^overeenkomsten/modelovereenkomsten/verwijderen/(?P<model_agreement_text_id>\d+)/$',
                      agreements.views.delete_model_agreement,
                      name='delete_model_agreement'),

                  url(r'^wachtwoord-vergeten/$', django.contrib.auth.views.password_reset,
                      {'post_reset_redirect': '/wachtwoord-vergeten/klaar/'},
                      name="password_reset"),
                  url(r'^wachtwoord-vergeten/klaar/$',
                      django.contrib.auth.views.password_reset_done),
                  url(r'^wachtwoord-vergeten/instellen/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                      django.contrib.auth.views.password_reset_confirm,
                      {'post_reset_redirect': '/wachtwoord-vergeten/opnieuw-ingesteld/'},
                      name="password_reset_confirm"),
                  url(r'^wachtwoord-vergeten/opnieuw-ingesteld/$',
                      django.contrib.auth.views.password_reset_complete),

                  url(r'^api/', include(router.urls)),
                  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  url(r'^markdownx/', include(markdownx))

              ] + static(conf.settings.STATIC_URL, document_root=conf.settings.STATIC_ROOT) + static(
    conf.settings.MEDIA_URL, document_root=conf.settings.MEDIA_ROOT)

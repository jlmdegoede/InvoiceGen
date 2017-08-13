from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
import settings.views

urlpatterns = [
    url(r'^$', settings.views.settings, name='settings'),
    url(r'^persoonlijk$', settings.views.PersonalSettings.as_view(),
        name='personal_settings'),
    url(r'^nieuwe-gebruiker$', settings.views.UserSettings.as_view(),
        name='create_new_user'),
    url(r'^gebruiker/bewerken/(?P<user_id>\d+)/$', settings.views.EditUserView.as_view(),
        name='edit_user'),
    url(r'^gebruiker/verwijderen$', settings.views.delete_user, name='delete_user'),
    url(r'^factuursjabloon/standaard$', settings.views.save_default_invoice_template,
        name='default_invoice'),
    url(r'^bunq-opslaan', settings.views.save_bunq_settings,
        name='save_bunq_settings'),
]

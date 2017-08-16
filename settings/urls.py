from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
import settings.views

urlpatterns = [
    url(r'^$', permission_required('settings.change_setting')(settings.views.PersonalSettings.as_view()),
        name='settings'),
    url(r'^factuursjablonen/$', permission_required('settings.change_setting')(settings.views.InvoiceTemplateSettings.as_view()),
            name='invoicetemplate_settings'),
    url(r'^gebruikers/$', permission_required('settings.change_setting')(settings.views.UserSettings.as_view()),
                name='user_settings'),
    url(r'^algemeen/$', permission_required('settings.change_setting')(settings.views.GeneralSettings.as_view()),
                name='general_settings'),

    url(r'^gebruiker/bewerken/(?P<user_id>\d+)/$', settings.views.EditUserView.as_view(),
        name='edit_user'),
    url(r'^gebruiker/verwijderen$', settings.views.delete_user, name='delete_user'),
]

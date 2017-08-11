from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
import agreements.views

urlpatterns = [
    url(r'^$', agreements.views.agreement_index,
        name='agreement_index'),
    url(r'^modelovereenkomsten/nieuw/$', permission_required('agreements.add_agreementtext')(agreements.views.AddAgreementText.as_view()),
        name='add_agreement_text'),
    url(r'^nieuw/$', agreements.views.add_agreement,
        name='add_agreement'),
    url(r'^ondertekenen/(?P<url>\w+)/$', agreements.views.view_agreement,
        name='view_agreement'),
    url(r'^ondertekenen/contractor/(?P<url>\w+)/$',
        agreements.views.sign_agreement_contractor,
        name='sign_contractor'),
    url(r'^ondertekenen/client/(?P<url>\w+)/$', agreements.views.sign_agreement_client,
        name='sign_client'),
    url(r'^verwijderen/(?P<agreement_id>\d+)/$', agreements.views.delete_agreement,
        name='delete_agreement'),
    url(r'^modelovereenkomsten/$', agreements.views.agreementtext_index,
        name='agreementtext_index'),
    url(r'^modelovereenkomsten/bewerken/(?P<model_agreement_id>\d+)/$',
        permission_required('agreements.change_agreementtext')(agreements.views.EditAgreementText.as_view()),
        name='edit_model_agreement'),
    url(r'^modelovereenkomsten/verwijderen/(?P<model_agreement_text_id>\d+)/$',
        agreements.views.delete_model_agreement,
        name='delete_model_agreement'),
]


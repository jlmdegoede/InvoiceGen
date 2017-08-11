from base64 import b64decode

import invoicegen.settings
import settings.helper
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views import View
from django.shortcuts import *
from django.utils import timezone
from django.utils.crypto import get_random_string
from django_tables2 import RequestConfig
from django.forms import formset_factory

from .tables import AgreementTable, AgreementTextTable
from .helper import replace_text
from .forms import AgreementForm, AgreementTextForm, AgreementTextVariableForm
from .models import *


@login_required
@permission_required('agreements.view_agreement')
def agreement_index(request):
    agreements = AgreementTable(Agreement.objects.all())
    RequestConfig(request).configure(agreements)
    return render(request, 'agreements/agreements.html', {'agreements': agreements})


@login_required
@permission_required('agreements.view_agreementtext')
def agreementtext_index(request):
    model_agreements = AgreementTextTable(AgreementText.objects.all())
    RequestConfig(request).configure(model_agreements)
    return render(request, 'agreements/agreementtext/agreementtext_index.html',
                  {'model_agreements': model_agreements})


@login_required
@permission_required('agreements.add_agreement')
def add_agreement(request):
    if request.method == 'POST':
        agreement = Agreement()
        agreement_form = AgreementForm(request.POST, instance=agreement)
        if agreement_form.is_valid():
            data = agreement_form.cleaned_data
            agreement_form.save(commit=False)
            agreement.created = timezone.now()
            agreement.url = get_random_string(length=32)
            agreement.agreement_text_copy = replace_text(agreement.agreement_text.text, data['article_concerned'])
            agreement.company = data['company']
            agreement.save()
            for article in data['article_concerned']:
                agreement.article_concerned.add(article)
            agreement.save()
            request.session['toast'] = 'Overeenkomst toegevoegd'
            return redirect(reverse('agreement_index'))
        else:
            return render(request, 'agreements/new_edit_agreement.html',
                          {'toast': 'Formulier onjuist ingevuld', 'form': agreement_form})
    else:
        form = AgreementForm()
        articles = Product.objects.filter(done=False)
        return render(request, 'agreements/new_edit_agreement.html', {'form': form, 'articles': articles})


def view_agreement(request, url):
    agreement = Agreement.objects.get(url=url)
    agreement.complete_url = 'https://' + invoicegen.settings.ALLOWED_HOSTS[
        0] + '/overeenkomsten/ondertekenen/' + agreement.url
    agreement.full_name = settings.helper.get_user_fullname()
    if request.method == 'GET':
        return render(request, 'agreements/view_sign_agreement.html', {'agreement': agreement})


@login_required
@permission_required('agreements.change_agreement')
def sign_agreement_contractor(request, url):
    agreement = Agreement.objects.get(url=url)
    if request.method == 'POST':
        if 'signature' in request.POST and 'signee_name' in request.POST and request.POST[
                'signee_name'].strip() and request.POST['signee_name'].strip():
            image_data = request.POST['signature'].split(',')
            image_data = b64decode(image_data[1])
            now = timezone.now()
            file_name = 'signature-of-' + request.POST['signee_name'] + '-at-' + str(now) + '.png'
            agreement.signature_file_contractor = ContentFile(image_data, file_name)
            agreement.signed_by_contractor_at = now
            agreement.signed_by_contractor = True
            agreement.save()
            agreement.complete_url = 'https://' + invoicegen.settings.ALLOWED_HOSTS[
                0] + '/overeenkomsten/ondertekenen/' + agreement.url
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Naam of handtekening ontbreekt'})


def sign_agreement_client(request, url):
    agreement = Agreement.objects.get(url=url)
    if request.method == 'POST':
        if 'signature' in request.POST and 'signee_name' in request.POST and request.POST[
                'signee_name'].strip() and request.POST['signee_name'].strip():
            image_data = request.POST['signature'].split(',')
            image_data = b64decode(image_data[1])
            now = timezone.now()
            file_name = 'signature-of-' + request.POST['signee_name'] + '-at-' + str(now) + '.png'
            agreement.signature_file_client = ContentFile(image_data, file_name)
            agreement.signed_by_client_at = now
            agreement.signed_by_client = True
            agreement.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Naam of handtekening ontbreekt'})


def send_push_notification_signed_agreement():
    pass


@login_required
@permission_required('agreements.delete_agreement')
def delete_agreement(request, agreement_id=-1):
    try:
        agreement_to_delete = Agreement.objects.get(id=agreement_id)
        agreement_to_delete.delete()
        request.session['toast'] = 'Overeenkomst verwijderd'
        return redirect(reverse('agreement_index'))
    except:
        request.session['toast'] = 'Verwijderen mislukt'
        return redirect(reverse('agreement_index'))


@login_required
@permission_required('agreements.delete_agreementtext')
def delete_model_agreement(request, model_agreement_text_id=-1):
    try:
        agreement_text_to_delete = AgreementText.objects.get(id=model_agreement_text_id)
        agreement_text_to_delete.delete()
        request.session['toast'] = 'Modelvereenkomst verwijderd'
        return redirect(reverse('agreementtext_index'))
    except:
        request.session['toast'] = 'Verwijderen mislukt'
        return redirect(reverse('agreementtext_index'))


class EditAgreementText(View):
    def post(self, request, model_agreement_id):
        agreementtext = AgreementText.objects.get(id=model_agreement_id)
        form = AgreementTextForm(request.POST, instance=agreementtext)
        if form.is_valid():
            form.save()
            variable_list = get_extra_variables(request)
            agreementtext.variables.add(*variable_list)
            agreementtext.save()
            return redirect(reverse('agreementtext_index'))
        else:
            return render(request, 'agreements/agreementtext/edit_agreementtext.html',
                          {'form': form, 'edit': True, 'error': form.errors,
                           'model_agreement_id': agreementtext.id})

    def get(self, request, model_agreement_id):
        model_agreement = AgreementText.objects.get(id=model_agreement_id)
        form = AgreementTextForm(instance=model_agreement)
        return render(request, 'agreements/agreementtext/edit_agreementtext.html',
                      {'form': form, 'model_agreement_id': model_agreement.id})


class AddAgreementText(View):
    def post(self, request):
        agree_text = AgreementText()
        agree_text_form = AgreementTextForm(request.POST, instance=agree_text)
        if agree_text_form.is_valid():
            agree_text_form.save(commit=False)
            agree_text.edited_at = timezone.now()
            agree_text.save()
            variable_list = get_extra_variables(request)
            agree_text.variables.add(*variable_list)
            agree_text.save()
            request.session['toast'] = 'Modelovereenkomst toegevoegd'
            return redirect(reverse('agreementtext_index'))
        else:
            return render(request, 'agreements/agreementtext/new_agreementtext.html',
                          {'toast': 'Formulier onjuist ingevuld', 'form': agree_text_form,
                           'error': agree_text_form.errors})

    def get(self, request):
        form = AgreementTextForm()
        return render(request, 'agreements/agreementtext/new_agreementtext.html', {'form': form})

def get_extra_variables(request):
    var_obj = request.POST['var_name1']
    counter = 1
    variable_list = []
    while var_obj is not None:
        desc_variable_name = 'desc' + str(counter)
        desc = request.POST[desc_variable_name]
        variable = AgreementTextVariable(name=var_obj, description=desc)
        variable.save()
        variable_list.append(variable)
        counter += 1
        key_variable_name = 'var_name' + str(counter)
        if key_variable_name in request.POST:
            var_obj = request.POST[key_variable_name]
        else:
            var_obj = None
    return variable_list

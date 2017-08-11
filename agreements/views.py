from base64 import b64decode

import invoicegen.settings
import settings.helper
from agreements.forms import AgreementForm, AgreementTextForm
from agreements.models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import *
from django.utils import timezone
from django.utils.crypto import get_random_string
from django_tables2 import RequestConfig

from .tables import AgreementTable, AgreementTextTable
from .models import AgreementTextVariable
from .helper import replace_text


@login_required
@permission_required('agreements.view_agreement')
def agreement_index(request):
    agreements = AgreementTable(Agreement.objects.all())
    RequestConfig(request).configure(agreements)
    return render(request, 'agreements/agreements.html', {'agreements': agreements})


@login_required
@permission_required('agreements.view_agreementtext')
def index_model_agreements(request):
    model_agreements = AgreementTextTable(AgreementText.objects.all())
    RequestConfig(request).configure(model_agreements)
    return render(request, 'agreements/model_agreements.html', {'model_agreements': model_agreements})


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
            return redirect('/overeenkomsten/')
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
        return redirect('/overeenkomsten')
    except:
        request.session['toast'] = 'Verwijderen mislukt'
        return redirect('/overeenkomsten')


@login_required
@permission_required('agreements.delete_agreementtext')
def delete_model_agreement(request, model_agreement_text_id=-1):
    try:
        agreement_text_to_delete = AgreementText.objects.get(id=model_agreement_text_id)
        agreement_text_to_delete.delete()
        request.session['toast'] = 'Modelvereenkomst verwijderd'
        return redirect('/overeenkomsten/modelovereenkomsten')
    except:
        request.session['toast'] = 'Verwijderen mislukt'
        return redirect('/overeenkomsten/modelovereenkomsten')



@login_required
@permission_required('agreements.change_agreementtext')
def edit_model_agreement(request, model_agreement_id):
    if request.method == 'POST':
        model_agreement = AgreementText.objects.get(id=model_agreement_id)
        form = AgreementTextForm(request.POST, instance=model_agreement)
        if form.is_valid():
            form.save()
            return redirect('/overeenkomsten')
        else:
            return render(request, 'agreements/new_edit_agreement_text.html',
                          {'form': form, 'edit': True, 'error': form.errors,
                           'model_agreement_id': model_agreement.id})
    else:
        try:
            model_agreement = AgreementText.objects.get(id=model_agreement_id)
            form = AgreementTextForm(instance=model_agreement)
            return render(request, 'agreements/new_edit_agreement_text.html',
                          {'form': form, 'edit': True, 'model_agreement_id': model_agreement.id})
        except:
            return redirect(to=index_model_agreements)


@login_required
@permission_required('agreements.add_agreementtext')
def add_agreement_text(request):
    if request.method == 'POST':
        agree_text = AgreementText()
        agree_text_form = AgreementTextForm(request.POST, instance=agree_text)
        if agree_text_form.is_valid():
            agree_text_form.save(commit=False)
            agree_text.edited_at = timezone.now()

            var_obj = request.POST['var_name1']
            variable_list = []
            while var_obj is not None:
                desc = request.POST['desc1']
                variable = AgreementTextVariable(name=var_obj, description=desc)
                variable.save()
                variable_list.append(variable)
                

            agree_text.save()
            request.session['toast'] = 'Modelovereenkomst toegevoegd'
            return redirect('/overeenkomsten')
        else:
            return render(request, 'agreements/new_edit_agreement_text.html',
                          {'toast': 'Formulier onjuist ingevuld', 'form': agree_text_form,
                           'error': agree_text_form.errors})
    else:
        form = AgreementTextForm()
        return render(request, 'agreements/new_edit_agreement_text.html', {'form': form})

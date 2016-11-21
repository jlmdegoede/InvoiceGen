from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from Agreements.models import *
from Agreements.forms import AgreementTextForm, AgreementForm, SignatureForm
import datetime
from Orders.models import Company
from Settings.models import UserSetting
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from base64 import b64decode
from django.core.files.base import ContentFile
import InvoiceGen.site_settings
import Settings.views
from .tables import AgreementTable, AgreementTextTable
from django_tables2 import RequestConfig

CLIENT_NAME_CONSTANT = '<NAAM_OPDRACHTGEVER>'
CLIENT_CITY_ZIPCODE_CONSTANT = '<POSTCODE_PLAATS_OPDRACHTGEVER>'
CLIENT_ADDRESS_CONSTANT = '<ADRES_OPDRACHTGEVER>'
CLIENT_COMPANY_NAME_CONSTANT = '<NAAM_OPDRACHTGEVER>'

CONTRACTOR_NAME_CONSTANT = '<MIJN_NAAM>'
CONTRACTOR_CITY_ZIPCODE_CONSTANT = '<MIJN_POSTCODE_EN_WOONPLAATS>'
CONTRACTOR_ADDRESS_CONSTANT = '<MIJN_ADRES>'

OPDRACHT_OMSCHRIJVING_CONSTANT = '<OMSCHRIJVING_OPDRACHT>'

AGREED_TEXT_CONSTANT = 'Ik ga akkoord'



@login_required
def agreement_index(request):
    agreements = AgreementTable(Agreement.objects.all())
    RequestConfig(request).configure(agreements)
    return render(request, 'Agreements/agreements.html', {'agreements': agreements})


@login_required
def index_model_agreements(request):
    model_agreements = AgreementTextTable(AgreementText.objects.all())
    RequestConfig(request).configure(model_agreements)
    return render(request, 'Agreements/model_agreements.html', {'model_agreements': model_agreements})


@login_required
def add_agreement(request):
    if request.method == 'POST':
        agreement = Agreement()
        agreement_form = AgreementForm(request.POST, instance=agreement)
        if agreement_form.is_valid():
            data = agreement_form.cleaned_data
            agreement_form.save(commit=False)
            agreement.created = datetime.datetime.now()
            agreement.url = get_random_string(length=32)
            agreement.agreement_text_copy = replace_text(agreement.agree_text.text, data['article_concerned'])
            agreement.company = data['company']
            agreement.save()
            for article in data['article_concerned']:
                agreement.article_concerned.add(article)
            agreement.save()
            request.session['toast'] = 'Overeenkomst toegevoegd'
            return redirect('/overeenkomsten/')
        else:
            return render(request, 'Agreements/new_edit_agreement.html',
                          {'toast': 'Formulier onjuist ingevuld', 'form': agreement_form})
    else:
        form = AgreementForm()
        articles = Product.objects.filter(done=False)
        return render(request, 'Agreements/new_edit_agreement.html', {'form': form, 'articles': articles})



def view_agreement(request, url):
    agreement = Agreement.objects.get(url=url)
    agreement.complete_url = 'https://' + InvoiceGen.site_settings.ALLOWED_HOSTS[
        0] + '/overeenkomsten/ondertekenen/' + agreement.url
    agreement.full_name = Settings.views.get_user_fullname()
    if request.method == 'GET':
        return render(request, 'Agreements/view_sign_agreement.html', {'agreement': agreement})


@login_required
def sign_agreement_contractor(request, url):
    agreement = Agreement.objects.get(url=url)
    if request.method == 'POST':
        if 'signature' in request.POST and 'signee_name' in request.POST and request.POST[
            'signee_name'].strip() and request.POST['signee_name'].strip():
            image_data = request.POST['signature'].split(',')
            image_data = b64decode(image_data[1])
            now = datetime.datetime.now()
            file_name = 'signature-of-' + request.POST['signee_name'] + '-at-' + str(now) + '.png'
            agreement.signature_file_contractor = ContentFile(image_data, file_name)
            agreement.signed_by_contractor_at = now
            agreement.signed_by_contractor = True
            agreement.save()
            agreement.complete_url = 'https://' + InvoiceGen.site_settings.ALLOWED_HOSTS[
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
            now = datetime.datetime.now()
            file_name = 'signature-of-' + request.POST['signee_name'] + '-at-' + str(now) + '.png'
            agreement.signature_file_client = ContentFile(image_data, file_name)
            agreement.signed_by_client_at = now
            agreement.signed_by_client = True
            agreement.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Naam of handtekening ontbreekt'})


@login_required
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
def delete_model_agreement(request, model_agreement_text_id=-1):
    try:
        agreement_text_to_delete = AgreementText.objects.get(id=model_agreement_text_id)
        agreement_text_to_delete.delete()
        request.session['toast'] = 'Modelvereenkomst verwijderd'
        return redirect('/overeenkomsten/modelovereenkomsten')
    except:
        request.session['toast'] = 'Verwijderen mislukt'
        return redirect('/overeenkomsten/modelovereenkomsten')


def replace_text(agree_text, products):
    user = UserSetting.objects.first()
    company = Company.objects.first()
    client_name = company.company_name
    client_city_zipcode = company.company_city_and_zipcode
    client_company_name = company.company_name
    client_address = company.company_address
    contractor_name = user.name
    contractor_city_zipcode = user.city_and_zipcode
    contractor_address = user.address

    article_text = "\n"
    for product in products:
        article_text += "Opdracht " + product.title + " met een kwantiteit van " + str(
            product.quantity) + " en een prijs van " + str(
            product.price_per_quantity) + " euro per eenheid voor opdrachtgever " + product.from_company.company_name + "\n"

    agree_text = agree_text.replace(OPDRACHT_OMSCHRIJVING_CONSTANT, article_text)
    agree_text = agree_text.replace(CLIENT_NAME_CONSTANT, client_name)
    agree_text = agree_text.replace(CLIENT_CITY_ZIPCODE_CONSTANT, client_city_zipcode)
    agree_text = agree_text.replace(CLIENT_COMPANY_NAME_CONSTANT, client_company_name)
    agree_text = agree_text.replace(CLIENT_ADDRESS_CONSTANT, client_address)
    agree_text = agree_text.replace(CONTRACTOR_ADDRESS_CONSTANT, contractor_address)
    agree_text = agree_text.replace(CONTRACTOR_CITY_ZIPCODE_CONSTANT, contractor_city_zipcode)
    agree_text = agree_text.replace(CONTRACTOR_NAME_CONSTANT, contractor_name)
    return agree_text


@login_required
def edit_model_agreement(request, model_agreement_id):
    if request.method == 'POST':
        model_agreement = AgreementText.objects.get(id=model_agreement_id)
        form = AgreementTextForm(request.POST, instance=model_agreement)
        if form.is_valid():
            form.save()
            return redirect('/overeenkomsten')
        else:
            return render(request, 'Agreements/new_edit_agreement_text.html', {'form': form, 'edit': True, 'error': form.errors,
                                                                       'model_agreement_id': model_agreement.id})
    else:
        try:
            model_agreement = AgreementText.objects.get(id=model_agreement_id)
            form = AgreementTextForm(instance=model_agreement)
            return render(request, 'Agreements/new_edit_agreement_text.html',
                          {'form': form, 'edit': True, 'model_agreement_id': model_agreement.id})
        except:
            return redirect(to=index_model_agreements)


@login_required
def add_agreement_text(request):
    if request.method == 'POST':
        agree_text = AgreementText()
        agree_text_form = AgreementTextForm(request.POST, instance=agree_text)
        if agree_text_form.is_valid():
            agree_text_form.save(commit=False)
            agree_text.edited_at = datetime.datetime.now()
            agree_text.save()
            request.session['toast'] = 'Modelovereenkomst toegevoegd'
            return redirect('/overeenkomsten')
        else:
            return render(request, 'Agreements/new_edit_agreement_text.html',
                          {'toast': 'Formulier onjuist ingevuld', 'form': agree_text_form,
                                       'error': agree_text_form.errors})
    else:
        form = AgreementTextForm()
        return render(request, 'Agreements/new_edit_agreement_text.html', {'form': form})

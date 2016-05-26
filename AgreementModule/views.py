from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from AgreementModule.models import *
from AgreementModule.forms import AgreementTextForm, AgreementForm
import datetime
import string
import random
from FactuurMaker.models import UserSetting, Company

# Create your views here.
CLIENT_NAME_CONSTANT = '[CLIENT_NAME]'
CLIENT_CITY_ZIPCODE_CONSTANT = '[CLIENT_CITY_ZIPCODE]'
CLIENT_ADDRESS_CONSTANT = '[CLIENT_ADDRESS]'
CLIENT_COMPANY_NAME_CONSTANT = '[CLIENT_COMPANY_NAME]'

CONTRACTOR_NAME_CONSTANT = '[CONTRACTOR_NAME]'
CONTRACTOR_CITY_ZIPCODE_CONSTANT = '[CONTRACTOR_CITY_ZIPCODE]'
CONTRACTOR_ADDRESS_CONSTANT = '[CONTRACTOR_ADDRESS]'

OPDRACHT_OMSCHRIJVING_CONSTANT = '[OPDRACHT-OMSCHRIJVING]'

AGREED_TEXT_CONSTANT = 'Ik ga akkoord'

@login_required
def add_agreement_text(request):
    context = RequestContext(request)
    if request.method == 'POST':
        agree_text = AgreementText()
        agree_text_form = AgreementTextForm(request.POST, instance=agree_text)
        if agree_text_form.is_valid():
            agree_text_form.save(commit=False)
            agree_text.edited_at = datetime.datetime.now()
            agree_text.save()
            request.session['toast'] = 'Modelovereenkomst toegevoegd'
            return redirect('/')
        else:
            return render_to_response('new_edit_agreement_text.html',
                                      {'toast': 'Formulier onjuist ingevuld', 'form': agree_text_form}, context)
    else:
        form = AgreementTextForm()
        return render_to_response('new_edit_agreement_text.html', {'form': form}, context)


@login_required
def add_agreement(request):
    context = RequestContext(request)
    if request.method == 'POST':
        agreement = Agreement()
        agreement_form = AgreementForm(request.POST, instance=agreement)
        if agreement_form.is_valid():
            data = agreement_form.cleaned_data
            agreement_form.save(commit=False)
            agreement.created = datetime.datetime.now()
            agreement.url = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(7))
            agreement.agreement_text_copy = replace_text(agreement.agree_text.text, data['article_concerned'])
            agreement.save()
            for article in data['article_concerned']:
                agreement.article_concerned.add(article)
            agreement.save()
            request.session['toast'] = 'Overeenkomst toegevoegd'
            return redirect('/agreements/')
        else:
            return render_to_response('new_edit_agreement.html',
                                      {'toast': 'Formulier onjuist ingevuld', 'form': agreement_form}, context)
    else:
        form = AgreementForm()
        articles = Product.objects.filter(done=False)
        return render_to_response('new_edit_agreement.html', {'form': form, 'articles': articles,}, context)


@login_required
def agreement_index(request):
    context = RequestContext(request)
    agreements = Agreement.objects.all()
    return render_to_response('agreements.html', {'agreements': agreements}, context)


def view_agreement(request, url):
    context = RequestContext(request)
    agreement = Agreement.objects.get(url=url)
    if request.method == 'GET':
        return render_to_response('view_sign_agreement.html', {'agreement': agreement }, context)
    if request.method == 'POST':
        if 'emailaddress' in request.POST and 'agreed' in request.POST:
            agreed_text = request.POST['agreed']
            emailaddress = request.POST['emailaddress']
            if agreement.client_emailaddress == emailaddress and agreed_text == AGREED_TEXT_CONSTANT:
                agreement.signed_by_client = True
                agreement.signed_by_client_at = datetime.datetime.now()
                agreement.save()
                return render_to_response('view_sign_agreement.html', {'agreement': agreement }, context)
            else:

                return render_to_response('view_sign_agreement.html', {'agreement': agreement, 'error': 'Incorrect e-mailadres/akkoordfrase'}, context)


def replace_text(agree_text, products):
    user = UserSetting.objects.first()
    company = Company.objects.first()
    client_name = company.bedrijfsnaam
    client_city_zipcode = company.bedrijfsplaats_en_postcode
    client_company_name = company.bedrijfsnaam
    client_address = company.bedrijfsadres
    contractor_name = user.naam
    contractor_city_zipcode = user.plaats_en_postcode
    contractor_address = user.adres

    article_text = "\n"
    for product in products:
        article_text += "Opdracht " + product.title + " met een hoeveelheid van " + str(product.quantity) + " en een prijs van " + str(product.price_per_quantity) + " euro per eenheid voor opdrachtgever " + product.from_company.bedrijfsnaam + "\n"

    agree_text = agree_text.replace(OPDRACHT_OMSCHRIJVING_CONSTANT, article_text)
    agree_text = agree_text.replace(CLIENT_NAME_CONSTANT, client_name)
    agree_text = agree_text.replace(CLIENT_CITY_ZIPCODE_CONSTANT, client_city_zipcode)
    agree_text = agree_text.replace(CLIENT_COMPANY_NAME_CONSTANT, client_company_name)
    agree_text = agree_text.replace(CLIENT_ADDRESS_CONSTANT, client_address)
    agree_text = agree_text.replace(CONTRACTOR_ADDRESS_CONSTANT, contractor_address)
    agree_text = agree_text.replace(CONTRACTOR_CITY_ZIPCODE_CONSTANT, contractor_city_zipcode)
    agree_text = agree_text.replace(CONTRACTOR_NAME_CONSTANT, contractor_name)
    return agree_text

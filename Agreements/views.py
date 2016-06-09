from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from Agreements.models import *
from Agreements.forms import AgreementTextForm, AgreementForm
import datetime
import string
import random
from Orders.models import Company
from Settings.models import UserSetting

# Create your views here.
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
def add_agreement(request):
    context = RequestContext(request)
    if request.method == 'POST':
        agreement = Agreement()
        agreement_form = AgreementForm(request.POST, instance=agreement)
        if agreement_form.is_valid():
            data = agreement_form.cleaned_data
            agreement_form.save(commit=False)
            agreement.created = datetime.datetime.now()
            agreement.url = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(9))
            agreement.agreement_text_copy = replace_text(agreement.agree_text.text, data['article_concerned'])
            agreement.company = data['company']
            agreement.save()
            for article in data['article_concerned']:
                agreement.article_concerned.add(article)
            agreement.save()
            request.session['toast'] = 'Overeenkomst toegevoegd'
            return redirect('/overeenkomsten/')
        else:
            return render_to_response('new_edit_agreement.html',
                                      {'toast': 'Formulier onjuist ingevuld', 'form': agreement_form}, context)
    else:
        form = AgreementForm()
        articles = Product.objects.filter(done=False)
        return render_to_response('new_edit_agreement.html', {'form': form, 'articles': articles}, context)


@login_required
def agreement_index(request):
    context = RequestContext(request)
    agreements = Agreement.objects.all()
    return render_to_response('agreements.html', {'agreements': agreements}, context)


def view_agreement(request, url):
    context = RequestContext(request)
    agreement = Agreement.objects.get(url=url)
    if request.method == 'GET':
        return render_to_response('view_sign_agreement.html', {'agreement': agreement}, context)
    if request.method == 'POST':
        if 'emailaddress' in request.POST and 'agreed' in request.POST:
            agreed_text = request.POST['agreed']
            emailaddress = request.POST['emailaddress']
            if agreement.client_emailaddress == emailaddress and agreed_text.lower() == AGREED_TEXT_CONSTANT.lower():
                agreement.signed_by_client = True
                agreement.signed_by_client_at = datetime.datetime.now()
                agreement.save()
                return render_to_response('view_sign_agreement.html', {'agreement': agreement}, context)
            else:

                return render_to_response('view_sign_agreement.html', {'agreement': agreement, 'error': 'Incorrect e-mailadres/akkoordfrase'}, context)


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
        article_text += "Opdracht " + product.title + " met een kwantiteit van " + str(product.quantity) + " en een prijs van " + str(product.price_per_quantity) + " euro per eenheid voor opdrachtgever " + product.from_company.company_name + "\n"

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
def index_model_agreements(request):
    context = RequestContext(request)
    model_agreements = AgreementText.objects.all()
    return render_to_response('model_agreements.html', {'model_agreements': model_agreements}, context)


@login_required
def edit_model_agreement(request, model_agreement_id):
    context = RequestContext(request)
    if request.method == 'POST':
        model_agreement = AgreementText.objects.get(id=model_agreement_id)
        form = AgreementTextForm(request.POST, instance=model_agreement)
        if form.is_valid():
            form.save()
            return redirect('/overeenkomsten')
        else:
            return render_to_response('new_edit_agreement_text.html', {'form': form, 'edit': True, 'error': form.errors, 'model_agreement_id': model_agreement.id}, context)
    else:
        try:
            model_agreement = AgreementText.objects.get(id=model_agreement_id)
            form = AgreementTextForm(instance=model_agreement)
            return render_to_response('new_edit_agreement_text.html', {'form': form, 'edit': True, 'model_agreement_id': model_agreement.id}, context)
        except:
            return redirect(to=index_model_agreements)


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
            return redirect('/overeenkomsten')
        else:
            return render_to_response('new_edit_agreement_text.html',
                                      {'toast': 'Formulier onjuist ingevuld', 'form': agree_text_form, 'error': agree_text_form.errors}, context)
    else:
        form = AgreementTextForm()
        return render_to_response('new_edit_agreement_text.html', {'form': form}, context)


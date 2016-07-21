from datetime import date

import markdown
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import *
from Invoices.models import *
from Agreements.models import Agreement
from Companies.forms import CompanyForm
from Orders.forms import *
from Utils.search_query import get_query
from Todo.views import create_task_from_order
from Settings.views import get_setting
import Settings.views
from django.core import serializers
import asyncio
from HourRegistration.models import HourRegistration
from .tables import OrderTable
from django_tables2 import RequestConfig
# Create your views here.


@login_required
def index(request):
    products = {}
    year_list = []
    years = Product.objects.values("date_deadline").distinct()

    for distinct_years in years:
        year = distinct_years['date_deadline'].year
        if year not in year_list:
            year_list.append(year)
            products_year = Product.objects.filter(date_deadline__contains=year, done=True)

            for product in products_year:
                agreements = Agreement.objects.filter(article_concerned=product)
                if agreements.count() != 0:
                    product.agreement = agreements[0]

            products[year] = OrderTable(products_year)
            RequestConfig(request).configure(products[year])

    toast = None
    if request.session.get('toast'):
        toast = request.session.get('toast')
        del request.session['toast']

    year_list.sort(reverse=True)

    active_products_table = OrderTable(Product.objects.filter(done=False))
    currentYear = date.today().year
    no_settings = Settings.views.no_settings_created_yet()

    RequestConfig(request).configure(active_products_table)

    return render(request, 'index.html',
                  {'products': products, 'active_products_table': active_products_table, 'toast': toast, 'years': year_list,
                   'currentYear': currentYear, 'first_time': no_settings})




@login_required
def view_product(request, productid):
    try:
        product = Product.objects.get(id=productid)
        if Agreement.objects.filter(article_concerned=product).count() != 0:
            product.agreement = Agreement.objects.filter(article_concerned=product)[0]
        hourregistration = HourRegistration.objects.filter(product=product)
        total_hours = 0
        for hour in hourregistration:
            if hour.end is not None:
                total_hours += ((hour.end - hour.start).total_seconds()).real
        total_hours = round((total_hours / 60) / 60, 2)
        return render(request, 'view_product.html', {'product': product, 'hourregistrations': hourregistration, 'total_hours': total_hours})
    except Exception as err:
        print(err)
        request.session['toast'] = 'Product niet gevonden'
        return redirect('/')

@login_required
def mark_products_as_done(request):
    if request.method == 'POST':
        for productId in request.POST.getlist('products[]'):
            product = Product.objects.get(id=productId)
            product.done = True
            product.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def view_statistics(request):
    year = date.today().year
    year_list = [int(year) - 5, int(year) - 4, int(year) - 3, int(year) - 2, int(year) - 1, int(year)]
    nr_of_articles = []
    not_yet_invoiced = []
    nr_of_words = []
    totale_inkomsten = []
    for i in range(int(year) - 5, int(year) + 1):
        tuple = get_yearly_stats(i)
        nr_of_articles.append(tuple[0])
        nr_of_words.append(tuple[1])
        totale_inkomsten.append(tuple[2])
        not_yet_invoiced.append(tuple[3])
    return render(request, 'statistics.html',
                  {'nr_of_articles': nr_of_articles, 'not_yet_invoiced': not_yet_invoiced, 'nr_of_words': nr_of_words,
                   'totale_inkomsten': totale_inkomsten, 'year': year, 'year_list': year_list})


def get_yearly_stats(year):
    nr_of_articles = 0
    totale_inkomsten = 0
    nr_of_words = 0
    all_articles = Product.objects.filter(done=True)
    for article in all_articles:
        if article.date_deadline.year == int(year):
            totale_inkomsten += article.quantity * article.price_per_quantity
            nr_of_words += article.quantity
            nr_of_articles += 1
    not_yet_invoiced = 0
    not_yet_invoiced_articles = Product.objects.filter(done=False)
    for article in not_yet_invoiced_articles:
        not_yet_invoiced += article.quantity * article.price_per_quantity

    return nr_of_articles, nr_of_words, totale_inkomsten, not_yet_invoiced


@login_required
def add_company_inline(request):
    context = RequestContext(request)
    if request.method == 'POST':
        company = Company()
        f = CompanyForm(request.POST, instance=company)
        if f.is_valid():
            company.save()
            request.session['toast'] = 'Bedrijf toegevoegd'
            return JsonResponse({'company_id': company.id, 'company_name': company.company_name})
    if request.method == 'GET':
        form = CompanyForm()
        return render_to_response('new_company_inline.html', {'form': form}, context)


@login_required
def add_article(request):
    context = RequestContext(request)
    if request.method == 'POST':
        article = Product()
        f = ProductForm(request.POST, instance=article)
        article.invoice = None
        if f.is_valid():
            article.save()
            request.session['toast'] = 'Opdracht toegevoegd'
            if get_setting('auto_wunderlist', False):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(create_task_from_order(article))
                loop.close()
            return redirect('/')
        else:
            return render_to_response('new_edit_product.html',
                                      {'toast': 'Formulier onjuist ingevuld', 'form': f, 'error': f.errors}, context)
    else:
        form = ProductForm()

        return render_to_response('new_edit_product.html', {'form': form}, context)


@login_required
def edit_article(request, articleid=-1):
    context = RequestContext(request)
    if request.method == 'GET':
        try:
            article = Product.objects.get(id=articleid)
            f = ProductForm(instance=article)

            return render_to_response('new_edit_product.html',
                                      {'form': f, 'edit': True, 'articleid': articleid}, context)
        except:
            request.session['toast'] = 'Opdracht niet gevonden'
            return redirect('/')
    elif request.method == 'POST':
        article = Product.objects.get(id=articleid)
        f = ProductForm(request.POST, instance=article)

        if f.is_valid():
            f.save()
            request.session['toast'] = 'Opdracht gewijzigd'
            return redirect('/')
        else:
            return render_to_response('new_edit_product.html',
                                      {'form': f, 'edit': True, 'articleid': articleid, 'toast': 'Ongeldig formulier'},
                                      context)


@login_required
def delete_article(request, articleid=-1):
    try:
        article_to_delete = Product.objects.get(id=articleid)
        article_to_delete.delete()
        request.session['toast'] = 'Opdracht verwijderd'
        return redirect('/')
    except:
        request.session['toast'] = 'Verwijderen mislukt'
        return redirect('/')


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')


def user_login_placeholder_email(request):
    context = RequestContext(request)
    form = UserForm()
    return render_to_response('login.html', {'form': form, 'email': request.GET['email']}, context)


def user_login(request):
    context = RequestContext(request)
    form = UserForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            return render_to_response('login.html', {'error': "Ongeldige inloggegevens", 'form': form}, context)
    else:
        return render_to_response('login.html', {'form': form}, context)


@login_required
def get_list_of_orders_hourregistration(request):
    orders = Product.objects.filter(done=False)
    return HttpResponse(serializers.serialize('json', orders), content_type='json')


@login_required
def search(request):
    query_string = ''
    found_products = None
    found_agreements = None
    found_incoming_invoices = None
    found_outgoing_invoices = None
    found_companies = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        product_query = get_query(query_string, ['title', 'briefing'])
        agreement_query = get_query(query_string, ['agreement_text_copy', 'client_name', 'client_emailaddress', ])
        incoming_invoice_query = get_query(query_string, ['title', 'invoice_number', ])
        outgoing_invoice_query = get_query(query_string, ['title', 'invoice_number', 'to_company__company_name'])
        companies_query = get_query(query_string, ['company_name', 'company_address', 'company_city_and_zipcode'])

        found_products = Product.objects.filter(product_query).order_by('-date_received')
        found_agreements = Agreement.objects.filter(agreement_query).order_by('-created')
        found_incoming_invoices = IncomingInvoice.objects.filter(incoming_invoice_query).order_by('-date_created')
        found_outgoing_invoices = OutgoingInvoice.objects.filter(outgoing_invoice_query).order_by('-date_created')
        found_companies = Company.objects.filter(companies_query)

    return render_to_response('search_results.html',
                              {'query_string': query_string, 'found_products': found_products,
                               'found_agreements': found_agreements, 'found_incoming_invoices': found_incoming_invoices,
                               'found_outgoing_invoices': found_outgoing_invoices, 'found_companies': found_companies},
                              context_instance=RequestContext(request))

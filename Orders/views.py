from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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
from Utils.session_helper import get_toast_and_cleanup_session
from datetime import datetime
from django.template import Context

# Create your views here.


@login_required
def index(request):
    products, year_list = fill_product_table_per_year(request)

    toast = get_toast_and_cleanup_session(request)

    active_products_table = OrderTable(Product.objects.filter(done=False), prefix='openstaand-', order_by='date_deadline')
    no_settings_notification = Settings.views.no_settings_created_yet()

    RequestConfig(request).configure(active_products_table)

    return render(request, 'index.html',
                  {'products': products, 'active_products_table': active_products_table, 'toast': toast,
                   'years': year_list, 'first_time': no_settings_notification})


def fill_product_table_per_year(request):
    year_list = []
    products = {}

    now = datetime.now()

    for year in range(now.year - 5, now.year + 1):
        products_year = Product.objects.filter(date_deadline__contains=year, done=True)
        if products_year.count() is not 0:
            year_list.append(year)
            products_year = add_agreements_to_products(products_year)
            prefix = str(year) + '-'
            products[year] = OrderTable(products_year, prefix=prefix, order_by='-date_deadline')
            RequestConfig(request).configure(products[year])

    year_list.sort(reverse=True)
    return products, year_list


def add_agreements_to_products(products):
    for product in products:
        add_agreements_to_product(product)
    return products


def add_agreements_to_product(product):
    agreements = Agreement.objects.filter(article_concerned=product)
    if agreements.count() != 0:
        product.agreement = agreements[0]
    return product


@login_required
def view_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product = add_agreements_to_product(product)

        hour_registration = HourRegistration.objects.filter(product=product)
        total_hours = sum(((x.end - x.start).total_seconds()).real for x in hour_registration if x.end is not None)
        total_hours = round((total_hours / 60) / 60, 2)

        return render(request, 'view_product.html',
                      {'product': product, 'hourregistrations': hour_registration, 'total_hours': total_hours})
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
def add_company_inline(request):
    if request.method == 'POST':
        company = Company()
        f = CompanyForm(request.POST, instance=company)
        if f.is_valid():
            company.save()
            request.session['toast'] = 'Bedrijf toegevoegd'
            return JsonResponse({'company_id': company.id, 'company_name': company.company_name})
    if request.method == 'GET':
        form = CompanyForm()
        return render(request, 'new_company_inline.html', {'form': form})


@login_required
def add_product(request):
    context = Context(request)
    if request.method == 'POST':
        return add_product_post(request)
    return add_product_get(request)


def add_product_post(request):
    product = Product()
    f = ProductForm(request.POST, instance=product)
    product.invoice = None
    if f.is_valid():
        product.save()
        request.session['toast'] = 'Opdracht toegevoegd'
        if get_setting('auto_wunderlist', False):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(create_task_from_order(product))
            loop.close()
        return redirect('/')
    else:
        return render(request, 'new_edit_product.html',
                                  {'toast': 'Formulier onjuist ingevuld', 'form': f, 'error': f.errors})


def add_product_get(request):
    form = ProductForm()
    return render(request, 'new_edit_product.html', {'form': form})


@login_required
def edit_product(request, product_id=-1):
    if request.method == 'GET':
        return edit_product_get(request, product_id)
    return edit_product_post(request, product_id)


def edit_product_get(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        f = ProductForm(instance=product)
        return render(request, 'new_edit_product.html',
                                  {'form': f, 'edit': True, 'productid': product_id})
    except:
        request.session['toast'] = 'Opdracht niet gevonden'
        return redirect('/')


def edit_product_post(request, product_id):
    product = Product.objects.get(id=product_id)
    f = ProductForm(request.POST, instance=product)

    if f.is_valid():
        f.save()
        request.session['toast'] = 'Opdracht gewijzigd'
        return redirect('/')
    else:
        return render(request, 'new_edit_product.html',
                                  {'form': f, 'edit': True, 'productid': product_id, 'toast': 'Ongeldig formulier'})


@login_required
def delete_product(request, product_id=-1):
    try:
        product_to_delete = Product.objects.get(id=product_id)
        product_to_delete.delete()
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
    form = UserForm()
    return render(request, 'login.html', {'form': form, 'email': request.GET['email']})


def user_login(request):
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
            return render(request, 'login.html', {'error': "Ongeldige inloggegevens", 'form': form})
    else:
        return render(request, 'login.html', {'form': form})


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

    return render(request, 'search_results.html',
                              {'query_string': query_string, 'found_products': found_products,
                               'found_agreements': found_agreements, 'found_incoming_invoices': found_incoming_invoices,
                               'found_outgoing_invoices': found_outgoing_invoices, 'found_companies': found_companies})

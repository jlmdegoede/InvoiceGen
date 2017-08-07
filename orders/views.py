import asyncio
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
import django.core.serializers
from django.http import JsonResponse
from django.shortcuts import *
from django.utils import timezone
from django.views import View
from django_tables2 import RequestConfig
from rest_framework import serializers, viewsets

import settings.views
from agreements.models import Agreement
from companies.forms import CompanyForm
from hour_registration.models import HourRegistration
from invoices.models import *
from settings.views import get_setting
from statistics.views import get_total_hours, get_unique_hours
from utils.date_helper import get_today_string
from utils.search_query import get_query

from .forms import *
from .helper import (add_agreements_to_product, fill_product_table_per_year,
                     get_previous_years)
from .tables import OrderTable
from .serializer import ProductSerializer

# Create your views here.


@login_required
@permission_required('orders.view_product')
def index(request):
    now = timezone.now()
    years_back = now.year - 5
    products, year_list = fill_product_table_per_year(request, years_back)
    active_products_table = OrderTable(Product.objects.filter(done=False), prefix='openstaand-', order_by='date_deadline')
    no_settings_notification = settings.views.no_settings_created_yet()
    RequestConfig(request).configure(active_products_table)
    years_not_in_table = get_previous_years(years_back)
    return render(request, 'orders/index.html',
                  {'products': products, 'active_products_table': active_products_table,
                   'years': year_list, 'first_time': no_settings_notification,
                   'years_not_in_table': years_not_in_table})


@login_required
@permission_required('orders.view_product')
def view_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product = add_agreements_to_product(product)
    hour_registration = HourRegistration.objects.filter(product=product)
    total_hours = get_total_hours(datetime.now().year, hour_registration)
    today = get_today_string()
    return render(request, 'orders/view_product.html',
                  {'product': product, 'hourregistrations': hour_registration, 'total_hours': total_hours, 'today': today})


@login_required
@permission_required('orders.view_product')
def view_products_in_year(request, year):
    now = timezone.now()
    years_back = now.year - 5
    products = OrderTable(Product.objects.filter(date_deadline__year=year), order_by='-date_deadline')
    years_not_in_table = get_previous_years(years_back)
    return render(request, 'orders/view_productlist.html',
                  {'products': products, 'year': year,
                   'years_not_in_table': years_not_in_table})


@login_required
@permission_required('orders.change_product')
def mark_products_as_done(request):
    if request.method == 'POST':
        for productId in request.POST.getlist('products[]'):
            product = Product.objects.get(id=productId)
            product.done = True
            product.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
@permission_required('orders.add_product')
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
        return render(request, 'orders/new_company_inline.html', {'form': form})


class AddProductView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'orders/new_edit_product.html', {'form': form})

    def post(self, request):
        product = Product()
        f = ProductForm(request.POST, instance=product)
        product.invoice = None
        if f.is_valid():
            product.save()
            for file in request.FILES.getlist('attachments'):
                p = ProductAttachment(attachment=file)
                p.save()
                product.attachments.add(p)
            product.save()
            request.session['toast'] = 'Opdracht toegevoegd'
            return redirect('/')
        else:
            request.session['toast'] = 'Formulier onjuist ingevuld'
            return render(request, 'orders/new_edit_product.html',
                          {'form': f, 'error': f.errors})


class EditProductView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            f = ProductForm(instance=product)

            return render(request, 'orders/new_edit_product.html',
                          {'form': f, 'edit': True, 'productid': product_id})
        except:
            request.session['toast'] = 'Opdracht niet gevonden'
            return redirect('/')

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        f = ProductForm(request.POST, instance=product)

        if f.is_valid():
            product.save()
            for file in request.FILES.getlist('attachments'):
                p = ProductAttachment(attachment=file)
                p.save()
                product.attachments.add(p)
            product.save()
            request.session['toast'] = 'Opdracht gewijzigd'
            return redirect('/')
        else:
            request.session['toast'] = 'Ongeldig formulier'
            return render(request, 'orders/new_edit_product.html',
                          {'form': f, 'edit': True, 'productid': product_id})


@login_required
@permission_required('orders.delete_product')
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
@permission_required('orders.delete_product')
def delete_attachment(request):
    if request.POST:
        product_id = request.POST['product_id']
        product_attachment_id = request.POST['product_attachment_id']
        product_attachment = ProductAttachment.objects.get(id=product_attachment_id)
        product = Product.objects.get(id=product_id)
        product.attachments.remove(product_attachment)
        product.save()
        product_attachment.attachment.delete()
        product_attachment.delete()
        return JsonResponse({'deleted': True})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


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
            return render(request, 'orders/login.html', {'error': "Ongeldige inloggegevens", 'form': form})
    else:
        return render(request, 'orders/login.html', {'form': form})


@login_required
def get_list_of_orders_hourregistration(request):
    orders = Product.objects.filter(done=False)
    return HttpResponse(django.core.serializers.serialize('json', orders), content_type='json')


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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

from datetime import date, timedelta

from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import *
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views import View
from django_tables2 import RequestConfig
from rest_framework import viewsets

import mail.views
import utils.markdown_generator
from InvoiceGen.celery import app
from InvoiceGen.settings import BASE_DIR
from invoices.forms import *
from invoices.tasks import generate_pdf_task
from settings.localization_nl import get_localized_text
from settings.models import UserSetting
from utils.date_helper import *
from utils.docx_generation import *

from .models import *
from .serializer import OutgoingInvoiceSerializer
from .tables import *


@login_required
@permission_required('invoices.view_invoice')
def get_outgoing_invoices(request):
    dict = get_invoices('outgoing', request)
    return render(request, 'Invoices/outgoing_invoice_table.html', dict)


@login_required
@permission_required('invoices.view_invoice')
def get_incoming_invoices(request):
    dict = get_invoices('incoming', request)
    return render(request, 'Invoices/incoming_invoice_table.html', dict)


def get_invoices(invoice_objects, request):
    invoices = {}
    year_list = []
    if invoice_objects == 'outgoing':
        years = OutgoingInvoice.objects.values("date_created").distinct()
        objects = OutgoingInvoice.objects.all()
    else:
        years = IncomingInvoice.objects.values("date_created").distinct()
        objects = IncomingInvoice.objects.all()

    for dict in years:
        year = dict['date_created'].year
        if year not in year_list:
            year_list.append(year)

            invoice_year_objs = objects.filter(date_created__contains=year).order_by('-date_created')
            if invoice_objects == 'outgoing':
                for invoice_obj in invoice_year_objs:
                    products = Product.objects.filter(invoice=invoice_obj)
                    invoice_obj.products = products

            if invoice_objects == 'outgoing':
                invoices[year] = OutgoingInvoiceTable(invoice_year_objs)
            else:
                invoices[year] = IncomingInvoiceTable(invoice_year_objs)
            RequestConfig(request).configure(invoices[year])

    current_year = date.today().year
    return {'invoices': invoices,  'years': year_list, 'currentYear': current_year}


@login_required
@permission_required('invoices.add_outgoinginvoice')
def add_outgoing_invoice(request):
    if request.method == 'GET':
        invoice = OutgoingInvoice()
        f = OutgoingInvoiceForm(instance=invoice)

        return render(request, 'Invoices/new_edit_outgoing_invoice.html',
                      {'form': f, 'invoceid': invoice.id, 'edit': False})
    elif request.method == 'POST':
        invoice = OutgoingInvoice()
        f = OutgoingInvoiceForm(request.POST, instance=invoice)

        if f.is_valid():
            f.save(commit=False)
            invoice.date_created = timezone.now()

            products = f.cleaned_data['products']
            for product in products:
                invoice.to_company = product.from_company

            invoice.invoice_number = f.cleaned_data['invoice_number']
            invoice.save()
            add_invoice_to_products(invoice, products)

            request.session['toast'] = get_localized_text('INVOICE_CREATED')
            return redirect('/facturen')
        else:
            return render(request, 'Invoices/new_edit_outgoing_invoice.html',
                          {'form': f, 'invoceid': invoice.id, 'edit': False,
                                       'toast': "Formulier ongeldig!"})


def add_invoice_to_products(invoice, products):
    for product in products:
        product.invoice = invoice
        product.save()


def remove_invoice_from_products(products):
    for product in products:
        product.invoice = None
        product.save()


@login_required
def download_latest_generated_invoice(request, file_type, invoice_id):
    switcher = {"pdf": get_latest_pdf, "docx": get_latest_docx, "markdown": get_latest_markdown}
    return switcher[file_type](invoice_id)


def get_latest_pdf(invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    response = HttpResponse(open(BASE_DIR + "/templates/MaterialDesign/temp/main.pdf", 'rb').read())
    response['Content-Disposition'] = 'attachment; filename={0}.pdf'.format(invoice.title)
    response['Content-Type'] = 'application/pdf'
    return response


@login_required
def generate_pdf(request, invoice_id):
    task = generate_pdf_task.delay(invoice_id)
    return JsonResponse({'generate': 'started', 'task_id': task.task_id})


@login_required
def check_pdf_task_status(request, task_id):
    task = app.AsyncResult(task_id)
    return JsonResponse({'status': task.state})


def get_latest_markdown(invoice_id, tenant=None):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    products = Product.objects.filter(invoice=invoice)
    with_tax_rate = products[0].tax_rate != 0
    contents = utils.markdown_generator.create_markdown_file(invoice, UserSetting.objects.first(),
                                                             products[0].from_company,
                                                             get_today_string(),
                                                             products,
                                                             with_tax_rate)


    response = HttpResponse(contents, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=invoice{0}.md'.format(str(invoice.date_created))
    return response


def get_latest_docx(invoice_id, tenant=None):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    products = Product.objects.filter(invoice=invoice)
    user = UserSetting.objects.first()
    doc = generate_docx_invoice(invoice, user, products, products[0].tax_rate != 0)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    doc.save(response)
    response['Content-Disposition'] = 'attachment; filename={0}.docx'.format(invoice.title)
    return response


@login_required
def share_link_to_outgoing_invoice(request, invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    return_dict = {}
    if invoice.url is None:
        invoice.url = get_random_string(length=32)
        return_dict['url'] = request.build_absolute_uri(reverse('view_outgoing_invoice_guest', args=[invoice.url]))
    else:
        invoice.url = None
    invoice.save()
    return JsonResponse(return_dict)


def view_outgoing_invoice_guest(request, invoice_url):
    invoice = OutgoingInvoice.objects.get(url=invoice_url)
    return render(request, 'Invoices/view_outgoing_invoice.html', {'invoice': invoice})


@login_required
@permission_required('invoices.add_incominginvoice')
def add_incoming_invoice(request):
    if request.method == 'GET':
        invoice = IncomingInvoice()
        f = IncomingInvoiceForm(instance=invoice)

        return render(request, 'Invoices/new_edit_incoming_invoice.html',
                      {'form': f, 'invoceid': invoice.id, 'edit': False})
    elif request.method == 'POST':
        invoice = IncomingInvoice()
        f = IncomingInvoiceForm(request.POST, request.FILES, instance=invoice)

        if f.is_valid():
            f.save(commit=False)
            invoice.date_created = timezone.now()
            if 'invoice_file' in request.FILES:
                invoice.invoice_file = request.FILES['invoice_file']
            invoice.save()
            request.session['toast'] = get_localized_text('INVOICE_CREATED')
            return redirect('/facturen/inkomend')
        else:
            return render(request, 'Invoices/new_edit_incoming_invoice.html',
                          {'form': f, 'invoceid': invoice.id, 'edit': False,
                                       'toast': "Formulier ongeldig!"})


@login_required
@permission_required('invoices.view_invoice')
def detail_incoming_invoice(request, invoice_id):
    invoice = IncomingInvoice.objects.get(id=invoice_id)
    return render(request, 'Invoices/view_incoming_invoice.html', {'invoice': invoice})


@login_required
@permission_required('invoices.view_invoice')
def detail_outgoing_invoice(request, invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    return render(request, 'Invoices/view_outgoing_invoice.html', {'invoice': invoice})


@login_required
@permission_required('invoices.change_outgoinginvoice')
def edit_outgoing_invoice(request, invoiceid=-1):
    if request.method == 'GET':
        try:
            invoice = OutgoingInvoice.objects.get(id=invoiceid)
            f = OutgoingInvoiceForm(instance=invoice)
            products = Product.objects.filter(invoice=invoice)

            return render(request, 'Invoices/new_edit_outgoing_invoice.html',
                          {'form': f, 'products': products, 'edit': True,
                                       'invoiceid': invoiceid})
        except:
            request.session['toast'] = get_localized_text('INVOICE_NOT_FOUND')
            return redirect('/facturen')
    elif request.method == 'POST':
        invoice = OutgoingInvoice.objects.get(id=invoiceid)
        f = OutgoingInvoiceForm(request.POST, instance=invoice)
        old_products = Product.objects.filter(invoice=invoice)

        if f.is_valid():
            old_products = Product.objects.filter(invoice=invoice)
            remove_invoice_from_products(old_products)

            f.save()

            new_products = f.cleaned_data['products']
            add_invoice_to_products(invoice, new_products)

            request.session['toast'] = get_localized_text('CHANGED_INVOICE')
            return redirect('/facturen')
        else:
            return render(request, 'Invoices/new_edit_outgoing_invoice.html',
                          {'form': f, 'products': old_products, 'invoiceid': invoice.id, 'edit': True,
                                       'toast': get_localized_text('INVALID_FORM')})


@login_required
@permission_required('invoices.change_incominginvoice')
def edit_incoming_invoice(request, invoiceid=-1):
    if request.method == 'GET':
        try:
            invoice = IncomingInvoice.objects.get(id=invoiceid)
            f = IncomingInvoiceForm(instance=invoice)

            return render(request, 'Invoices/new_edit_incoming_invoice.html',
                          {'form': f, 'invoice': invoice, 'edit': True})
        except:
            request.session['toast'] = get_localized_text('INVOICE_NOT_FOUND')
            return redirect('/facturen/inkomend')
    elif request.method == 'POST':
        invoice = IncomingInvoice.objects.get(id=invoiceid)
        f = IncomingInvoiceForm(request.POST, request.FILES, instance=invoice)

        if f.is_valid():
            f.save()
            if 'invoice_file' in request.FILES:
                invoice.invoice_file = request.FILES['invoice_file']
            request.session['toast'] = get_localized_text('INVOICE_CHANGED')
            return redirect('/facturen/inkomend')
        else:
            return render(request, 'Invoices/new_edit_incoming_invoice.html',
                          {'form': f, 'invoiceid': invoice.id, 'edit': True,
                                       'toast': get_localized_text('INVALID_FORM')})


@login_required
@permission_required('invoices.delete_outgoinginvoice')
def delete_outgoing_invoice(request, invoiceid=-1):
    try:
        invoice = OutgoingInvoice.objects.get(id=invoiceid)
        articles = Product.objects.filter(invoice=invoice)
        for article in articles:
            article.invoice = None
            article.save()

        invoice.delete()
        request.session['toast'] = get_localized_text('DELETE_INVOICE_SUCCESS')
        return redirect('/facturen')
    except:
        request.session['toast'] = get_localized_text('DELETE_INVOICE_FAILED')
        return redirect('/facturen')


@login_required
@permission_required('invoices.delete_incominginvoice')
def delete_incoming_invoice(request, invoiceid=-1):
    try:
        invoice = IncomingInvoice.objects.get(id=invoiceid)
        invoice.delete()
        request.session['toast'] = get_localized_text('DELETE_INVOICE_SUCCESS')
        return redirect('/facturen/inkomend')
    except:
        request.session['toast'] = get_localized_text('DELETE_INVOICE_FAILED')
        return redirect('/facturen/inkomend')


@login_required
def generate_invoice(request):
    if request.method == 'POST':
        products = []
        totaalbedrag = 0
        invoice = OutgoingInvoice()
        for product_id in request.POST.getlist('products[]'):
            product = Product.objects.get(id=product_id)
            products.append(product)
            totaalbedrag += product.quantity * product.price_per_quantity

        today = get_today_string()
        volgnummer = request.POST.get('volgnummer')
        invoice.invoice_number = volgnummer
        # create invoice and save it
        invoice.date_created = datetime.date.today()
        invoice.title = "Factuur {0}".format(str(today))
        invoice.to_company = products[0].from_company
        invoice.expiration_date = timezone.now() + timedelta(days=14)
        invoice.save()

        for product in products:
            product.invoice = invoice
            product.save()
        return JsonResponse({'return_url': reverse(detail_outgoing_invoice, kwargs={'invoice_id': invoice.id})})
    return JsonResponse({'success': False})


class SendOutgoingInvoicePerEmail(View):
    def get(self, request, invoice_id):
        invoice = OutgoingInvoice.objects.get(id=invoice_id)
        return mail.views.get_email_form(request, to=invoice.to_company.company_email, invoice_id=invoice_id)


class OutgoingInvoiceViewSet(viewsets.ModelViewSet):
    queryset = OutgoingInvoice.objects.all()
    serializer_class = OutgoingInvoiceSerializer

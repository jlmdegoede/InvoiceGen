from datetime import date, timedelta

from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import *
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views import View
from rest_framework import viewsets

import mail.views
from Invoicegen.celery import app
from invoices.forms import *
from invoices.tasks import task_generate_pdf
from settings.localization_nl import get_localized_text
from utils.date_helper import *

from .models import *
from .serializer import OutgoingInvoiceSerializer
from .tables import *
from .helper import get_invoices, add_invoice_to_products, remove_invoice_from_products, get_docx_invoice, \
    get_markdown_invoice, get_pdf_invoice


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


class AddOutgoingInvoice(View):
    def get(self, request):
        invoice = OutgoingInvoice()
        f = OutgoingInvoiceForm(instance=invoice)

        return render(request, 'Invoices/new_edit_outgoing_invoice.html',
                      {'form': f, 'invoiceid': invoice.id, 'edit': False})

    def post(self, request):
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
                          {'form': f, 'invoiceid': invoice.id, 'edit': False,
                           'toast': "Formulier ongeldig!"})


@login_required
def download_latest_generated_invoice(request, file_type, invoice_id):
    switcher = {"pdf": get_pdf_invoice, "docx": get_docx_invoice, "markdown": get_markdown_invoice}
    return switcher[file_type](invoice_id)


@login_required
def generate_pdf(request, invoice_id):
    task = task_generate_pdf.delay(invoice_id)
    return JsonResponse({'generate': 'started', 'task_id': task.task_id})


@login_required
def check_pdf_task_status(request, task_id):
    task = app.AsyncResult(task_id)
    return JsonResponse({'status': task.state})


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
                      {'form': f, 'invoiceid': invoice.id, 'edit': False})
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
                          {'form': f, 'invoiceid': invoice.id, 'edit': False,
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


class EditOutgoingInvoice(View):
    def get(self, request, invoice_id=-1):
        try:
            invoice = OutgoingInvoice.objects.get(id=invoice_id)
            f = OutgoingInvoiceForm(instance=invoice)
            products = Product.objects.filter(invoice=invoice)

            return render(request, 'Invoices/new_edit_outgoing_invoice.html',
                          {'form': f, 'products': products, 'edit': True,
                           'invoice_id': invoice_id})
        except:
            request.session['toast'] = get_localized_text('INVOICE_NOT_FOUND')
            return redirect('/facturen')

    def post(self, request, invoice_id=-1):
        invoice = OutgoingInvoice.objects.get(id=invoice_id)
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
                          {'form': f, 'products': old_products, 'invoice_id': invoice.id, 'edit': True,
                           'toast': get_localized_text('INVALID_FORM')})


class EditIncomingInvoice(View):
    def get(self, request, invoice_id=-1):
        try:
            invoice = IncomingInvoice.objects.get(id=invoice_id)
            f = IncomingInvoiceForm(instance=invoice)

            return render(request, 'Invoices/new_edit_incoming_invoice.html',
                          {'form': f, 'invoice': invoice, 'edit': True})
        except:
            request.session['toast'] = get_localized_text('INVOICE_NOT_FOUND')
            return redirect('/facturen/inkomend')

    def post(self, request, invoice_id=-1):
        invoice = IncomingInvoice.objects.get(id=invoice_id)
        f = IncomingInvoiceForm(request.POST, request.FILES, instance=invoice)

        if f.is_valid():
            f.save()
            if 'invoice_file' in request.FILES:
                invoice.invoice_file = request.FILES['invoice_file']
            request.session['toast'] = get_localized_text('INVOICE_CHANGED')
            return redirect('/facturen/inkomend')
        else:
            return render(request, 'Invoices/new_edit_incoming_invoice.html',
                          {'form': f, 'invoice_id': invoice.id, 'edit': True,
                           'toast': get_localized_text('INVALID_FORM')})


@login_required
@permission_required('invoices.delete_outgoinginvoice')
def delete_outgoing_invoice(request, invoice_id=-1):
    try:
        invoice = OutgoingInvoice.objects.get(id=invoice_id)
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
def delete_incoming_invoice(request, invoice_id=-1):
    try:
        invoice = IncomingInvoice.objects.get(id=invoice_id)
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

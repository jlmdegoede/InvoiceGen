from datetime import date, timedelta

from django.shortcuts import HttpResponse
from django_tables2 import RequestConfig

import utils.markdown_generator
from InvoiceGen.settings import BASE_DIR
from orders.models import Product
from settings.models import UserSetting
from utils.date_helper import *
from utils.docx_generation import *

from .models import IncomingInvoice, OutgoingInvoice
from .tables import IncomingInvoiceTable, OutgoingInvoiceTable


def add_invoice_to_products(invoice, products):
    for product in products:
        product.invoice = invoice
        product.save()


def remove_invoice_from_products(products):
    for product in products:
        product.invoice = None
        product.save()


def get_latest_pdf(invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    response = HttpResponse(open(BASE_DIR + "/templates/MaterialDesign/temp/main.pdf", 'rb').read())
    response['Content-Disposition'] = 'attachment; filename={0}.pdf'.format(invoice.title)
    response['Content-Type'] = 'application/pdf'
    return response


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

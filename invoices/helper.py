from datetime import date

from django.shortcuts import HttpResponse
from django_tables2 import RequestConfig

from InvoiceGen.settings import BASE_DIR
from orders.models import Product
from settings.const import DEFAULT_DOCX
from settings.helper import get_setting

from .models import IncomingInvoice, OutgoingInvoice, InvoiceTemplate
from .tables import IncomingInvoiceTable, OutgoingInvoiceTable
from .export.export import WordExport, MarkdownExport


def add_invoice_to_products(invoice, products):
    for product in products:
        product.invoice = invoice
        product.save()


def remove_invoice_from_products(products):
    for product in products:
        product.invoice = None
        product.save()


def get_pdf_invoice(invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    invoice_file_path = BASE_DIR + "/temp/" + invoice.title + ".pdf"
    response = HttpResponse(open(invoice_file_path, 'rb').read())
    response['Content-Disposition'] = 'attachment; filename={0}.pdf'.format(invoice.title)
    response['Content-Type'] = 'application/pdf'
    return response


def get_markdown_invoice(invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    products = Product.objects.filter(invoice=invoice)
    invoice_template = InvoiceTemplate.objects.filter(template_type=InvoiceTemplate.MARKDOWN).first()
    markdown = MarkdownExport(invoice, products, invoice_template)
    markdown.generate()
    response = HttpResponse(open(markdown.output_filepath(), 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=invoice{0}.md'.format(str(invoice.date_created))
    return response


def get_docx_invoice(invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    products = Product.objects.filter(invoice=invoice)
    default_docx_template = get_setting(DEFAULT_DOCX, 2)
    invoice_template = InvoiceTemplate.objects.get(id=default_docx_template)
    doc = WordExport(invoice, products, invoice_template)
    doc.generate()
    response = HttpResponse(open(doc.output_filepath(), 'rb').read())
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
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

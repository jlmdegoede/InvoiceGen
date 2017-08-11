# Create your tasks here
from __future__ import absolute_import, unicode_literals

from Invoicegen.celery import app
from orders.models import Product
from settings.helper import get_setting
from settings.const import DEFAULT_PDF

from .models import OutgoingInvoice, InvoiceTemplate
from .export.export import LatexExport


@app.task
def task_generate_pdf(invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    products = Product.objects.filter(invoice=invoice)
    default_pdf = int(get_setting(DEFAULT_PDF, 1))
    template = InvoiceTemplate.objects.get(id=default_pdf)
    pdf = LatexExport(invoice, products, template)
    pdf.generate()
    pdf = None  # trigger GC
    return True

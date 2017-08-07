# Create your tasks here
from __future__ import absolute_import, unicode_literals

from InvoiceGen.celery import app
from orders.models import Product
from settings.models import UserSetting
from utils.pdf_generation import *

from .models import OutgoingInvoice


@app.task
def generate_pdf_task(invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    products = Product.objects.filter(invoice=invoice)
    user = UserSetting.objects.first()
    generate_pdf(products, user, invoice)
    return True

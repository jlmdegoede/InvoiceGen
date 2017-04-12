# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from .models import OutgoingInvoice
from Settings.models import UserSetting
from Orders.models import Product
from Utils.pdf_generation import *
from django.shortcuts import *
from InvoiceGen.settings import BASE_DIR
from InvoiceGen.celery import app
from channels import Channel
import json


@app.task
def generate_pdf_task(invoice_id, reply_channel):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    products = Product.objects.filter(invoice=invoice)
    user = UserSetting.objects.first()
    generate_pdf(products, user, invoice)
    if reply_channel is not None:
        Channel(reply_channel).send({
            "text": json.dumps ({
                "action": "completed",
                "url": "/download-invoice"
            })
        })

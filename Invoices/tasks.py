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
from django.db import connection
from django.shortcuts import get_object_or_404
from Tenants.models import Client


@app.task
def generate_pdf_task(invoice_id, tenant):
    tenant = get_object_or_404(Client, schema_name=tenant)
    connection.set_tenant(tenant=tenant)

    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    products = Product.objects.filter(invoice=invoice)
    user = UserSetting.objects.first()
    generate_pdf(products, user, invoice)
    return True

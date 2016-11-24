# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from Settings.models import UserSetting
from Orders.models import Product
from Utils.pdf_generation import *
from django.shortcuts import *
from InvoiceGen.settings import BASE_DIR
from channels import Channel
import json
from Invoices.tasks import generate_pdf_task


@task
def send_email(email, attach_pdf=False):
    django_email = new_email.convert_to_django_email()

    if attach_pdf:
        attachment = open(BASE_DIR + "/InvoiceTemplates/MaterialDesign/temp/main.pdf", 'rb')
        django_email.attach(invoice.title, attachment.read(), 'application/pdf')
    if DEBUG is False:
        django_email.send(fail_silently=False)
    else:
        print(django_email)

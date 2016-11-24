# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from django.shortcuts import *
import json
from Invoices.tasks import generate_pdf_task
from django.utils import timezone
from .models import Email
from InvoiceGen.settings import BASE_DIR
from InvoiceGen.site_settings import DEBUG

@task
def send_email(email_id):
    new_email = Email.objects.get(id=email_id)
    django_email = new_email.convert_to_django_email()

    if new_email.document_attached:
        attachment = open(BASE_DIR + "/InvoiceTemplates/MaterialDesign/temp/main.pdf", 'rb')
        django_email.attach('Factuur.pdf', attachment.read(), 'application/pdf')
    if DEBUG is False:
        django_email.send(fail_silently=False)
    else:
        print(django_email)
    new_email.sent = True
    new_email.sent_at = timezone.now()
    new_email.save()

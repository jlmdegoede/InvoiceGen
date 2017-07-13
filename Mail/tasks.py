# Create your tasks here
from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from .models import Email
from InvoiceGen.settings import BASE_DIR
from InvoiceGen.celery import app
from celery.result import AsyncResult


@app.task
def send_email(previous_task_success, email_id):
    if previous_task_success:
        new_email = Email.objects.get(id=email_id)
        django_email = new_email.convert_to_django_email()

        if new_email.document_attached:
            attachment = open(BASE_DIR + "/InvoiceTemplates/MaterialDesign/temp/main.pdf", 'rb')
            django_email.attach('Factuur.pdf', attachment.read(), 'application/pdf')
        django_email.send(fail_silently=False)
        new_email.sent = True
        new_email.sent_at = timezone.now()
        new_email.save()

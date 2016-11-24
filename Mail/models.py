from django.db import models
from django.core.mail import EmailMessage

# Create your models here.

class Email(models.Model):
    subject = models.CharField(max_length=100)
    to = models.EmailField()
    cc = models.EmailField(null=True)
    bcc = models.EmailField(null=True)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)
    document_attached = models.BooleanField(default=False)

    def convert_to_django_email(self):
        return EmailMessage(self.subject, self.contents,
                            'no-reply@invoicegen.nl', [self.to], [self.bcc],
                            cc=[self.cc])

class EmailTemplate(models.Model):
    subject = models.CharField(max_length=100)
    contents = models.TextField()

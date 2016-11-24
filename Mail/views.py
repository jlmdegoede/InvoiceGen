from django.shortcuts import render
from django.views import View
from django.core.mail import EmailMessage
from InvoiceGen.site_settings import DEBUG

# Create your views here.

class SendOutgoingObjectPerEmail(View):
    def get(self, request):
        email_form = EmailForm()
        invoice = OutgoingInvoice.objects.get(id=invoice_id)
        return render(request, 'Mail/email_invoice.html', {'form': email_form, 'invoice': invoice})

    def post(self, request):
        email_form = EmailForm(instance=request.POST)
        email_form.save()
        if email_form.is_valid():
            subject = email_form.cleaned_data['subject']
            to = email_form.cleaned_data['to']
            contents = email_form.cleaned_data['contents']
            bcc = email_form.cleaned_data['bcc']
            cc = email_form.cleaned_data['cc']
            email = EmailMessage(subject, contents, 'no-reply@invoicegen.nl', [to], [bcc], cc=[cc])
            if DEBUG is False:
                email.send(fail_silently=False)
            else: print(email)

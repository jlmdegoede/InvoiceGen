from django.shortcuts import render
from django.views import View
from InvoiceGen.site_settings import DEBUG
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from .tables import EmailTemplateTable
from django.shortcuts import *

# Create your views here.
def get_email_form(to=None, template_to_use=None):
    initial_values = {}
    if template_to_use is not None:
        initial_values = {'subject': template_to_use.subject, 'contents': template_to_use, 'to': to}
    email_form = EmailForm(initial=initial_values)
    return render(request, 'Mail/email_invoice.html', {'form': email_form})

def add_url_to_contents_template(url, template_contents):
    return template_contents.replace('[url]', url)

def add_invoice_title_to_subject(invoice_title, template_contents):
    return template_contents.replace('[titel]', invoice_title)

@login_required
def save_and_send_email(request):
    new_email = Email()
    email_form = EmailForm(request.POST, instance=new_email)
    if email_form.is_valid():
        new_email.save()
        django_email = new_email.convert_to_django_email()
        if DEBUG is False: django_email.send(fail_silently=False)
        else: print(django_email)

@login_required
def list_view_templates(request):
    template_table = EmailTemplateTable(EmailTemplate.objects.all())
    return render(request, 'Mail/email_template_list.html', {'template_table': template_table})

class NewEditEmailTemplate(View):
    def get(self, request, email_template_id=0):
        email_template = self.get_email_template_instance(email_template_id)
        email_template_form = EmailTemplateForm(instance=email_template)
        return render(request, 'Mail/new_edit_email_template.html', {'form': email_template_form})

    def get_email_template_instance(self, email_template_id=0):
        return EmailTemplate() if email_template_id is 0 else EmailTemplate.objects.get(id=email_template_id)

    def post(self, request, email_template_id=0):
        email_template = self.get_email_template_instance(email_template_id)
        email_template_form = EmailTemplateForm(request.POST, instance=email_template)
        if email_template_form.is_valid():
            email_template.save()
            return redirect(to=list_view_templates)
        else:
            return render(request, 'Mail/new_edit_email_template.html', {'form': email_template_form})

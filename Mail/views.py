from django.shortcuts import render
from django.views import View
from InvoiceGen.site_settings import DEBUG
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from .tables import EmailTemplateTable, EmailTable
from django.shortcuts import *
from .tasks import send_email
from django.http import JsonResponse

# Create your views here.
def get_email_form(request, to=None):
    initial_values = {'to': to}
    email_form = EmailForm(initial=initial_values)
    email_templates = EmailTemplate.objects.all()
    return render(request, 'Mail/email_invoice.html', {'form': email_form, 'emailtemplates': email_templates})

@login_required
def get_template(request):
    if request.POST and 'email_template_id' in request.POST:
        email_template_id = request.POST['email_template_id']
        email_template = EmailTemplate.objects.get(id=email_template_id)
        return JsonResponse({'subject': email_template.subject, 'contents': email_template.contents})

@login_required
def save_and_send_email(request):
    new_email = Email()
    email_form = EmailForm(request.POST, instance=new_email)
    if email_form.is_valid():
        new_email.save()
        send_email.delay(new_email)
    else: return render(request, 'Mail/email_invoice.html', {'form': email_form})

@login_required
def list_view_templates(request):
    template_table = EmailTemplateTable(EmailTemplate.objects.all())
    return render(request, 'Mail/email_template_list.html', {'template_table': template_table})

class NewEditEmailTemplate(View):
    def get(self, request, email_template_id=0):
        email_template = self.get_email_template_instance(email_template_id)
        email_template_form = EmailTemplateForm(instance=email_template)
        return render(request, 'Mail/new_edit_email_template.html', {'form': email_template_form, 'email_template_id': email_template_id})

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

class SentEmailListView(View):
    def get(self, request):
        emails = Email.objects.all()
        email_table = EmailTable(emails)
        return render(request, 'Mail/sent_emails.html', {'table': email_table})

@login_required
def get_email_contents(request, email_id):
    email = Email.objects.get(id=email_id)
    return JsonResponse({'contents': email.contents})

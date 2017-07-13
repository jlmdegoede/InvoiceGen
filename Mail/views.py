from django.views import View
from .forms import *
from django.contrib.auth.decorators import login_required
from .tables import EmailTemplateTable, EmailTable
from django.shortcuts import *
from .tasks import send_email
from django.http import JsonResponse
from Invoices.tasks import generate_pdf_task


def get_email_form(request, to=None, invoice_id=0):
    initial_values = {'to': to}
    email_form = EmailForm(initial=initial_values)
    email_templates = EmailTemplate.objects.all()
    return render(request, 'Mail/email_invoice.html', {'form': email_form, 'emailtemplates': email_templates,
                                                       'invoice_id': invoice_id})


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
    invoice_id = request.POST['invoice_id']
    if email_form.is_valid():
        new_email.save()
        if new_email.document_attached:
            request.session['toast'] = 'PDF wordt gemaakt'
            generate_pdf_task.apply_async([invoice_id], link=send_email.s(new_email.id))
        else:
            send_email.delay(True, new_email.id)
        request.session['toast'] = 'E-mail wordt verzonden'
        return redirect(reverse('detail_outgoing_invoice', args=[invoice_id]))
    else:
        email_templates = EmailTemplate.objects.all()
        return render(request, 'Mail/email_invoice.html', {'form': email_form, 'email_templates': email_templates, 'invoice_id': invoice_id})


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
def get_email_contents(request):
    if request.POST and 'email_id' in request.POST:
        email_id = request.POST['email_id']
        email = Email.objects.get(id=email_id)
        return JsonResponse({'contents': email.contents})


@login_required
def delete_email_template(request):
    if request.POST and 'email_template_id' in request.POST:
        email_template_id = request.POST['email_template_id']
        email_template = EmailTemplate.objects.get(id=email_template_id)
        email_template.delete()
        return JsonResponse({'success': True})


def create_and_send_email_without_form(to, subject, contents):
    email = Email(to=to, subject=subject, contents=contents)
    email.save()
    send_email.delay(True, email.id)

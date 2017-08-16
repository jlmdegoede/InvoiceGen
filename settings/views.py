from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import *
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views import View
from invoicegen.settings import DEFAULT_COLOR
from invoicegen.settings import ALLOWED_HOSTS
from invoices.models import InvoiceTemplate
from mail.views import create_and_send_email_without_form
from payment.providers.bunq import BunqApi

from .forms import *
from .models import *
from .localization_nl import get_localized_text
from .helper import get_setting, get_from_request_and_save_setting, save_setting, create_groups, add_user_to_groups
from .const import *


class UserSettings(View):
    def get(self, request):
        user_list = User.objects.all()
        return render(request, 'settings/user_settings.html',
                      {'user_list': user_list, 'new_user_form': UserForm()})

    def post(self, request):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            groups = user_form.cleaned_data['groups']
            password = get_random_string(20)
            new_user = User.objects.create_user(username, email, password)
            add_user_to_groups(new_user, groups)
            self.prepare_new_user_mail(email, username, password)
            return redirect(to='user_settings')
        else:
            return render(request, 'settings/user_settings.html', {'users': {'new_user_form': user_form}})

    def prepare_new_user_mail(self, email, username, password):
        subject = get_localized_text('NEW_USER_MAIL_SUBJECT')
        host = 'https://{0}'.format(ALLOWED_HOSTS[0])
        contents = get_localized_text('NEW_USER_MAIL_CONTENTS',
                                      {'[USER]': username, '[PASSWORD]': password, '[WEBSITE]': host})
        create_and_send_email_without_form(to=email, subject=subject, contents=contents)


@permission_required('settings.change_setting')
def delete_user(request):
    if request.POST and 'user_id' in request.POST:
        user_id = int(request.POST['user_id'])
        if user_id is not 1:
            user = User.objects.get(pk=user_id)
            user.delete()

            request.session['toast'] = get_localized_text(key='USER_DELETED')
            return redirect(to='user_settings')
        else:
            return JsonResponse({'error': get_localized_text('USER_DELETE_FIRST')})


class PersonalSettings(View):
    def get(self, request):
        user_i = UserSetting.objects.all().first()
        if not user_i:
            user_i = UserSetting()
        form = UserSettingForm(instance=user_i)
        return render(request, 'settings/personal_settings.html', {'form': form})

    @method_decorator(permission_required('settings.change_setting'))
    def post(self, request):
        try:
            user = UserSetting.objects.get(id=1)
        except:
            user = UserSetting()
        form = UserSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            request.session['toast'] = get_localized_text(key='SETTINGS_SAVED')
            return redirect(to='settings')
        else:
            return render(request, 'settings/personal_settings.html', {'form': form, 'error': form.errors})


class InvoiceTemplateSettings(View):
    def get(self, request):
        pdf_templates = InvoiceTemplate.objects.filter(template_type=InvoiceTemplate.LATEX)
        docx_templates = InvoiceTemplate.objects.filter(template_type=InvoiceTemplate.DOCX)
        default_pdf = get_setting(DEFAULT_PDF, 1)
        default_docx = get_setting(DEFAULT_DOCX, 2)
        return render(request, 'settings/invoice_settings.html',
                      {'templates': {'pdf': pdf_templates, 'docx': docx_templates},
                       'default_docx': int(default_docx), 'default_pdf': int(default_pdf)})

    def post(self, request):
        if request.POST:
            type = request.POST['type']
            template_id = request.POST['template_id']
            if 'pdf' in type:
                save_setting('pdf_default_template', template_id)
            elif 'docx' in type:
                save_setting('docx_default_template', template_id)
            return JsonResponse({'saved': True})


class EditUserView(View):
    @method_decorator(permission_required('settings.change_setting'))
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_form = UserForm(instance=user)
        return render(request, 'settings/edit_user.html', {'form': user_form, 'userid': user.id})

    @method_decorator(permission_required('settings.change_setting'))
    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            groups = user_form.cleaned_data['groups']
            user.username = username
            user.email = email
            user.groups.clear()  # delete existing groups
            add_user_to_groups(user, groups)  # before adding the new ones
            return redirect(to='user_settings')
        else:
            return render(request, 'settings/edit_user.html', {'users': {'new_user_form': user_form}})


class GeneralSettings(View):
    def get(self, request):
        return_dict = {}
        return_dict['site_name'] = get_setting(SITE_NAME, 'Invoicegen')
        return_dict['site_url'] = get_setting(SITE_URL, '')
        return_dict['color_up'] = get_setting(COLOR_UP, DEFAULT_COLOR)
        return_dict['color_down'] = get_setting(COLOR_DOWN, DEFAULT_COLOR)
        bunq_api_key = get_setting(BUNQ_API_KEY, '')
        return_dict['default_bunq_account'] = int(get_setting(DEFAULT_BUNQ_ACCOUNT, 0))
        bunq_accounts = None
        if bunq_api_key != '':
            bunq_accounts = BunqApi().monetary_accounts()
        return_dict['bunq_accounts'] = bunq_accounts
        return_dict['mollie_api_key'] = get_setting(MOLLIE_API_KEY, '')
        return_dict['bunq_api_key'] = bunq_api_key
        return render(request, 'settings/general_settings.html', return_dict)

    def post(self, request):
        get_from_request_and_save_setting(request, 'bunq_api_key', BUNQ_API_KEY)
        get_from_request_and_save_setting(request, 'defaultbunq', DEFAULT_BUNQ_ACCOUNT)
        get_from_request_and_save_setting(request, 'site_name', SITE_NAME)
        get_from_request_and_save_setting(request, 'site_url', SITE_URL)
        get_from_request_and_save_setting(request, 'color_up', COLOR_UP)
        get_from_request_and_save_setting(request, 'color_down', COLOR_DOWN)
        get_from_request_and_save_setting(request, 'mollie_api_key', MOLLIE_API_KEY)
        request.session['toast'] = get_localized_text(key='SETTINGS_SAVED')
        return redirect(to='general_settings')

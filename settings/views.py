import json

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
from settings.forms import *
from settings.models import *
from payment.providers.bunq import BunqApi

from .localization_nl import get_localized_text
from .helper import get_setting, save_website_name, save_colors, save_setting, create_groups, add_user_to_groups
from .const import *


@login_required
@permission_required('settings.change_setting')
def settings(request):
    return_dict = {
        'personal': PersonalSettings().get_personal_settings(request),
        'users': UserSettings().get_user_settings(request),
        'invoices': get_invoice_templates(),
        'settings': get_bunq_settings(),
    }
    create_groups()
    return render(request, 'settings/settings.html', return_dict)


class UserSettings(View):
    @method_decorator(permission_required('settings.change_setting'))
    def get_user_settings(self, request):
        user_list = User.objects.all()
        return {'user_list': user_list, 'new_user_form': UserForm()}

    @method_decorator(permission_required('settings.change_setting'))
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
            return redirect(to=settings)
        else:
            return render(request, 'settings/settings.html', {'users': {'new_user_form': user_form}})

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
            return redirect(to=settings)
        else:
            return JsonResponse({'error': get_localized_text('USER_DELETE_FIRST')})


class PersonalSettings(View):
    def get_personal_settings(self, request):
        user_i = UserSetting.objects.all().first()
        if not user_i:
            user_i = UserSetting()
        site_name = get_setting(SITE_NAME, 'invoicegen')
        form = UserSettingForm(instance=user_i, initial={'site_name': site_name})
        color_up = get_setting(COLOR_UP, DEFAULT_COLOR)
        color_down = get_setting(COLOR_DOWN, DEFAULT_COLOR)

        return {'form': form, 'color_up': color_up, 'color_down': color_down}

    @method_decorator(permission_required('settings.change_setting'))
    def post(self, request):
        try:
            user = UserSetting.objects.get(id=1)
        except:
            user = UserSetting()
        form = UserSettingForm(request.POST, instance=user)
        if form.is_valid():
            save_website_name(form)
            save_colors(form)
            form.save()
            request.session['toast'] = get_localized_text(key='SETTINGS_SAVED')
            return redirect(to=settings)
        else:
            color_up = get_setting(COLOR_UP, DEFAULT_COLOR)
            color_down = get_setting(COLOR_DOWN, DEFAULT_COLOR)
            return render(request, 'settings/settings.html',
                          {'personal': {'form': form, 'error': form.errors,
                                        'color_up': color_up, 'color_down': color_down}})


def get_invoice_templates():
    pdf_templates = InvoiceTemplate.objects.filter(template_type=InvoiceTemplate.LATEX)
    docx_templates = InvoiceTemplate.objects.filter(template_type=InvoiceTemplate.DOCX)
    default_pdf = get_setting(DEFAULT_PDF, 1)
    default_docx = get_setting(DEFAULT_DOCX, 2)
    return {'templates': {'pdf': pdf_templates, 'docx': docx_templates},
            'default_docx': int(default_docx), 'default_pdf': int(default_pdf)}


@login_required
def save_default_invoice_template(request):
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
            return redirect(to=settings)
        else:
            return render(request, 'settings/settings.html', {'users': {'new_user_form': user_form}})


@login_required
@permission_required('settings.change_setting')
def save_bunq_settings(request):
    if request.POST:
        api_key = request.POST['bunq_api_key']
        save_setting(BUNQ_API_KEY, api_key)
        default_bunq_account = request.POST['defaultbunq']
        save_setting(DEFAULT_BUNQ_ACCOUNT, default_bunq_account)
        return redirect(to=settings)


def get_bunq_settings():
    bunq_api_key = get_setting(BUNQ_API_KEY, '')
    default_bunq = int(get_setting(DEFAULT_BUNQ_ACCOUNT, 0))
    bunq_accounts = None
    if bunq_api_key != '':
        bunq_accounts = BunqApi().monetary_accounts()
    return {'bunq_api_key': bunq_api_key, 'default_bunq_account': default_bunq, 'accounts': bunq_accounts}
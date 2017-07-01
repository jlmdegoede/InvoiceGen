from django.shortcuts import *
from Settings.models import *
from Settings.forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
import json
from InvoiceGen.settings import DEFAULT_COLOR
from django.views import View
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .group_management import *
from .localization_nl import get_localized_text
from django.http import JsonResponse
from InvoiceGen.site_settings import ALLOWED_HOSTS
from Mail.views import create_and_send_email_without_form
# Create your views here.


def create_groups():
    create_agreement_group()
    create_company_group()
    create_invoice_group()
    create_order_group()
    create_settings_group()


class UserSettings(View):
    @method_decorator(permission_required('Settings.change_setting'))
    def get_user_settings(self, request):
        user_list = User.objects.all()
        return {'user_list': user_list, 'new_user_form': UserForm()}

    @method_decorator(permission_required('Settings.change_setting'))
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
            print('Gebruiker {0} met wachtwoord: {1}'.format(username, password))
            return redirect(to=settings)
        else:
            return render(request, 'Settings/settings.html', {'users': {'new_user_form': user_form}})

    def prepare_new_user_mail(self, email, username, password):
        subject = get_localized_text('NEW_USER_MAIL_SUBJECT')
        host = 'https://{0}'.format(ALLOWED_HOSTS[0])
        contents = get_localized_text('NEW_USER_MAIL_CONTENTS', {'[USER]': username, '[PASSWORD]': password, '[WEBSITE]': host})
        create_and_send_email_without_form(to=email, subject=subject, contents=contents)


@permission_required('Settings.change_setting')
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

        site_name = get_setting('site_name', 'InvoiceGen')
        form = UserSettingForm(instance=user_i, initial={'site_name': site_name})

        color_up = get_setting('color_up', DEFAULT_COLOR)
        color_down = get_setting('color_down', DEFAULT_COLOR)

        return {'form': form, 'color_up': color_up, 'color_down': color_down}

    @method_decorator(permission_required('Settings.change_setting'))
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
            color_up = get_setting('color_up', DEFAULT_COLOR)
            color_down = get_setting('color_down', DEFAULT_COLOR)
            return render(request, 'Settings/settings.html',
                          {'personal': {'form': form,  'error': form.errors,
                                        'color_up': color_up, 'color_down': color_down}})


@login_required
@permission_required('Settings.change_setting')
def settings(request):
    return_dict = {
        'personal': PersonalSettings().get_personal_settings(request),
        'users': UserSettings().get_user_settings(request),
    }
    create_groups()
    return render(request, 'Settings/settings.html', return_dict)


class EditUserView(View):
    @method_decorator(permission_required('Settings.change_setting'))
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_form = UserForm(instance=user)
        return render(request, 'Settings/edit_user.html', {'form': user_form, 'userid': user.id})

    @method_decorator(permission_required('Settings.change_setting'))
    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            groups = user_form.cleaned_data['groups']
            user.username = username
            user.email = email
            user.groups.clear() # delete existing groups
            add_user_to_groups(user, groups) # before adding the new ones
            return redirect(to=settings)
        else:
            return render(request, 'Settings/settings.html', {'users': {'new_user_form': user_form}})


def save_colors(form):
    color_up = form.cleaned_data['color_up']
    save_setting('color_up', color_up)
    color_down = form.cleaned_data['color_down']
    save_setting('color_down', color_down)


def convert_to_json_utf8(data):
    return json.dumps(data).encode('utf-8')


def get_wunderlist_lists():
    return Todo.views.get_lists()


def no_settings_created_yet():
    try:
        UserSetting.objects.get(id=1)
        return False
    except:
        return True


def get_user_fullname():
    try:
        user = UserSetting.objects.get(id=1)
        return user.name
    except:
        return ""


def get_setting(key, default_value):
    setting = Setting.objects.filter(key=key)
    if setting.count() is not 0:
        setting = setting[0].value
    else:
        setting = default_value
    return setting


def save_setting(key, value):
    setting = Setting.objects.filter(key=key)
    if setting.count() is not 0:
        setting = setting[0]
        setting.value = value
    else:
        setting = Setting()
        setting.key = key
        setting.value = value
    setting.save()
    return setting

def save_website_name(form):
    site_name_f = form.cleaned_data['site_name']
    site_name = Setting.objects.filter(key='site_name')

    if site_name is not None:
        if site_name.count() == 0:
            site_name = Setting(key='site_name', value=site_name_f)
        else:
            site_name = site_name[0]
            site_name.value = site_name_f
        site_name.save()

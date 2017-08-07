import json
from .group_management import *
from .models import UserSetting, Setting


def save_colors(form):
    color_up = form.cleaned_data['color_up']
    save_setting('color_up', color_up)
    color_down = form.cleaned_data['color_down']
    save_setting('color_down', color_down)


def convert_to_json_utf8(data):
    return json.dumps(data).encode('utf-8')


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


def create_groups():
    create_agreement_group()
    create_company_group()
    create_invoice_group()
    create_order_group()
    create_settings_group()

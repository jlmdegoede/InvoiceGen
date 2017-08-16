import json
from .group_management import *
from .models import UserSetting, Setting


def get_from_request_and_save_setting(request, key, setting_key):
    if key in request.POST:
        value = request.POST[key]
        save_setting(setting_key, value)


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


def create_groups():
    create_agreement_group()
    create_company_group()
    create_invoice_group()
    create_order_group()
    create_settings_group()

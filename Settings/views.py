from django.shortcuts import *
from Settings.models import *
from Settings.forms import *
from django.contrib.auth.decorators import login_required
from Todo.models import *
import json
import Todo.views
import requests
from InvoiceGen.site_settings import COMMUNICATION_KEY
# Create your views here.


@login_required
def settings(request):
    toast = ''
    if request.method == 'POST':
        try:
            user = UserSetting.objects.get(id=1)
        except:
            user = UserSetting()
        form = UserSettingForm(request.POST, instance=user)
        if form.is_valid():
            save_website_name(form)
            form.save()
            toast = 'Instellingen opgeslagen'
        else:
            return render(request, 'settings.html',
                          {'form': form, 'toast': toast, 'errors': form.errors})
    user_i = UserSetting.objects.all().first()

    if not user_i:
        user_i = UserSetting()

    site_name = get_setting('site_name', 'InvoiceGen')
    form = UserSettingForm(instance=user_i, initial={'site_name': site_name})

    color_form = ColorForm()
    lists = None
    current_list = None
    wunderlist_enabled = False
    todo = None
    wunderlist_dict = None
    invoice_site = get_current_settings()

    try:
        todo = TodoAuth.objects.get(id=1)
        lists = get_wunderlist_lists()
        current_list = get_setting('wunderlist', 0)
        wunderlist_enabled = get_setting('auto_wunderlist', False)
    except:
        print("Geen Wunderlist-integratie")
        wunderlist_dict = Todo.views.get_wunderlist_url(request)

    return render(request, 'settings.html',
                  {'form': form, 'color_form': color_form, 'toast': toast, 'todo': todo, 'lists': lists,
                   'wunderlist_dict': wunderlist_dict,
                   'current_list': current_list, 'wunderlist_enabled': wunderlist_enabled, 'invoice_site': invoice_site})


def get_current_settings():
    try:
        req = requests.post('https://invoicegen.nl/get-subscription-status/', {'key': COMMUNICATION_KEY}, {})
        return json.loads(req.content.decode('utf-8'))
    except:
        print("Error")

def convert_to_json_utf8(data):
    return json.dumps(data).encode('utf-8')


def get_wunderlist_lists():
    return Todo.views.get_lists()


def no_settings_created_yet():
    try:
        user = UserSetting.objects.get(id=1)
        return False
    except:
        return True

def get_user_fullname():
    try:
        user = UserSetting.objects.get(id=1)
        return user.name
    except:
        return ""


@login_required
def save_wunderlist_settings(request):
    if request.method == 'POST':
        if 'new_list' in request.POST and request.POST['new_list'] != "":
            # create new list
            json = Todo.views.create_new_list(request.POST['new_list'])
            save_setting('wunderlist', json['id'])
        else:
            selected_list = request.POST['existing_list']
            save_setting('wunderlist', selected_list)
        save_setting('auto_wunderlist', request.POST['auto_add_to_wunderlist'] == 'on')
    return redirect(to=settings)


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


@login_required
def set_colors(request):
    if request.method == 'POST':
        form = ColorForm(request.POST)
        if form.is_valid():
            color_up_f = form.cleaned_data['color_up']
            color_down_f = form.cleaned_data['color_down']

            color_up = Setting.objects.filter(key='color_up')
            color_down = Setting.objects.filter(key='color_down')

            if color_up is not None:
                if color_up.count() == 0:
                    color_up = Setting(key='color_up', value=color_up_f)
                else:
                    color_up = color_up[0]
                    color_up.value = color_up_f
                color_up.save()

            if color_down is not None:
                if color_down.count() == 0:
                    color_down = Setting(key='color_down', value=color_down_f)
                else:
                    color_down = color_down[0]
                    color_down.value = color_down_f
                color_down.save()
    return redirect(to='settings')


@login_required
def reset_colors(request):
    color_up = Setting.objects.filter(key='color_up')
    color_down = Setting.objects.filter(key='color_down')

    if color_up is not None:
        if color_up.count() == 0:
            color_up = Setting(key='color_up', value='#009688')
        else:
            color_up = color_up[0]
            color_up.value = '#009688'
        color_up.save()

    if color_down is not None:
        if color_down.count() == 0:
            color_down = Setting(key='color_down', value='#009688')
        else:
            color_down = color_down[0]
            color_down.value = '#009688'
        color_down.save()

    return redirect(to='settings')


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

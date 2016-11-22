from django.shortcuts import *
from Settings.models import *
from Settings.forms import *
from django.contrib.auth.decorators import login_required
from Todo.models import *
import json
import Todo.views
import requests
import pytz
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from InvoiceGen.site_settings import COMMUNICATION_KEY
from InvoiceGen.settings import DEFAULT_COLOR
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
            save_colors(form)
            form.save()
            toast = 'Instellingen opgeslagen'
        else:
            return render(request, 'Settings/settings.html',
                          {'form': form, 'toast': toast, 'error': form.errors})
    user_i = UserSetting.objects.all().first()

    if not user_i:
        user_i = UserSetting()

    site_name = get_setting('site_name', 'InvoiceGen')
    form = UserSettingForm(instance=user_i, initial={'site_name': site_name})

    lists = None
    current_list = None
    wunderlist_enabled = False
    todo = None
    wunderlist_dict = None
    invoice_site = get_current_settings_json()
    color_up = get_setting('color_up', DEFAULT_COLOR)
    color_down = get_setting('color_down', DEFAULT_COLOR)

    try:
        todo = TodoAuth.objects.get(id=1)
        lists = get_wunderlist_lists()
        current_list = get_setting('wunderlist', 0)
        wunderlist_enabled = get_setting('auto_wunderlist', False)
    except:
        print("Geen Wunderlist-integratie")
        wunderlist_dict = Todo.views.get_wunderlist_url(request)

    return render(request, 'Settings/settings.html',
                  {'form': form, 'toast': toast, 'todo': todo, 'lists': lists,
                   'wunderlist_dict': wunderlist_dict, 'color_up': color_up,
                   'current_list': current_list, 'wunderlist_enabled': wunderlist_enabled, 'invoice_site': invoice_site})

@login_required
def renew_subscription(request):
    print("Redirecting...")
    return HttpResponseRedirect('https://invoicegen.nl/betaling/start?key=' + COMMUNICATION_KEY)

def save_colors(form):
    color_up = form.cleaned_data['color_up']
    save_setting('color_up', color_up)
    color_down = form.cleaned_data['color_down']
    save_setting('color_down', color_down)

def get_current_settings_json():
    try:
        req = requests.post('https://invoicegen.nl/get-subscription-status/', {'key': COMMUNICATION_KEY}, {})
        utc = pytz.UTC
        values = json.loads(req.content.decode('utf-8'))
        print(values['valid_until'])
        valid_until = utc.localize(datetime.strptime(values['valid_until'], '%d-%m-%Y %H:%M:%S'))
        save_setting('subscription_date', valid_until)
        return values
    except Exception as e:
        print("Error: could not get subscription status:" + str(e))


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

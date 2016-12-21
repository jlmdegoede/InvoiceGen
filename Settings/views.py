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
from InvoiceGen.site_settings import COMMUNICATION_KEY
from InvoiceGen.settings import DEFAULT_COLOR
from django.views import View
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth.models import Group
# Create your views here.


class IntegrationSettings(View):

    def get_integration_settings(self, request):
        wunderlist_enabled = False
        todo = None
        wunderlist_dict = None
        lists = []
        current_list = None

        try:
            todo = TodoAuth.objects.get(id=1)
            lists = get_wunderlist_lists()
            current_list = get_setting('wunderlist', 0)
            wunderlist_enabled = get_setting('auto_wunderlist', False)
        except:
            print("Geen Wunderlist-integratie geactiveerd")
            wunderlist_dict = Todo.views.get_wunderlist_url(request)

        return {'todo': todo, 'lists': lists, 'wunderlist_dict': wunderlist_dict,
                       'current_list': current_list, 'wunderlist_enabled': wunderlist_enabled }

    def post(self, request):
        if 'new_list' in request.POST and request.POST['new_list'] != "":
            # create new list
            json = Todo.views.create_new_list(request.POST['new_list'])
            save_setting('wunderlist', json['id'])
        else:
            selected_list = request.POST['existing_list']
            save_setting('wunderlist', selected_list)
        save_setting('auto_wunderlist', request.POST['auto_add_to_wunderlist'] == 'on')
        return redirect(to=settings)


class UserSettings(View):

    def get_user_settings(self, request):
        user_list = User.objects.all()
        return {'user_list': user_list, 'new_user_form': UserForm()}

    def post(self, request):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = get_random_string(20)
            User.objects.create_user(username, email, password)
            print('Gebruiker {0} met wachtwoord: {1}'.format(username, password))
            return redirect(to=settings)
        else:
            return render(request, 'Settings/settings.html', {'new_user_form': user_form})


class SubscriptionSettings(View):

    def get_subscription_settings(self, request):
        invoice_site = get_current_settings_json()
        return {'invoice_site': invoice_site}


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
            request.session['toast'] = 'Instellingen opgeslagen'
            return redirect(to=settings)
        else:
            color_up = get_setting('color_up', DEFAULT_COLOR)
            color_down = get_setting('color_down', DEFAULT_COLOR)
            return render(request, 'Settings/settings.html',
                          {'personal': {'form': form,  'error': form.errors,
                                        'color_up': color_up, 'color_down': color_down}})


@login_required
def settings(request):
    return_dict = {}
    return_dict['personal'] = PersonalSettings().get_personal_settings(request)
    return_dict['users'] = UserSettings().get_user_settings(request)
    return_dict['integration'] = IntegrationSettings().get_integration_settings(request)
    return_dict['subscription'] = SubscriptionSettings().get_subscription_settings(request)
    return render(request, 'Settings/settings.html', return_dict)


class EditUserView(View):

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_form = UserForm(instance=user)
        return render(request, 'Settings/edit_user.html', {'form': user_form})


def create_user_group():
    product_group = Group.objects.get_or_create(name='Opdrachten')
    invoice_group = Group.objects.get_or_create(name='Facturen')
    agreements_group = Group.objects.get_or_create(name='Overeenkomsten')
    companies_group = Group.objects.get_or_create(name='Opdrachtgevers')
    hour_registration_group = Group.objects.get_or_create(name='Urenregistratie')
    email_group = Group.objects.get_or_create(name='E-mail')
    statistics_group = Group.objects.get_or_create(name='Statistieken')
    settings_group = Group.objects.get_or_create(name='Instellingen')

    #permission = Permission.objects.filter(codename='change_invoice')[1]
    #product_group[0].permissions.add(permission)
    #product_group[0].save()
    #user = User.objects.get(username='test1')
    #user.groups.add(product_group[0])
    #user.save()
    #print(user.has_perm('Invoices.view_invoice'))


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

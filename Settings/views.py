from django.shortcuts import *
from Settings.models import *
from Settings.forms import *
from django.contrib.auth.decorators import login_required
from Todo.models import *
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

    site_name = Setting.objects.filter(key='site_name')
    if site_name.count() is not 0:
        site_name = site_name[0].value
    else:
        site_name = 'InvoiceGen'
    form = UserSettingForm(instance=user_i, initial={'site_name': site_name})
    color_form = ColorForm()

    todo = None
    try:
        todo = TodoAuth.objects.get(id=1)
    except:
        print("Geen Wunderlist-integratie")

    return render(request, 'settings.html',
                  {'form': form, 'color_form': color_form, 'toast': toast, 'todo': todo})


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
            color_up = Setting(key='color_up', value='#607d8b')
        else:
            color_up = color_up[0]
            color_up.value = '#607d8b'
        color_up.save()

    if color_down is not None:
        if color_down.count() == 0:
            color_down = Setting(key='color_down', value='#e65100')
        else:
            color_down = color_down[0]
            color_down.value = '#e65100'
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
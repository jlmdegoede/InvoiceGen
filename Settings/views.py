from django.shortcuts import render
from Settings.models import *
from Settings.forms import *
from django.contrib.auth.decorators import login_required
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
            form.save()
            toast = 'Instellingen opgeslagen'
        else:
            return render(request, 'settings.html',
                          {'form': form, 'toast': toast, 'errors': form.errors})
    user_i = UserSetting.objects.all().first()
    if not user_i:
        user_i = UserSetting()
    form = UserSettingForm(instance=user_i)

    return render(request, 'settings.html',
                  {'form': form, 'toast': toast})


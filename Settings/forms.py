from django import forms
from django.contrib.auth.models import User
from django import forms
from Settings.models import UserSetting


class UserSettingForm(forms.ModelForm):
    class Meta:
        model = UserSetting
        fields = '__all__'

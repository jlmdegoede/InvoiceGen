from django import forms
from django.contrib.auth.models import User
from django import forms
from Settings.models import UserSetting


class UserSettingForm(forms.ModelForm):
    site_name = forms.CharField(label="Websitenaam", max_length=200)
    kvk = forms.CharField(label="Websitenaam", required=False)
    btw_number = forms.CharField(label="Websitenaam", required=False)
    color_up = forms.CharField(label="Kleur boven", required=False)
    color_down = forms.CharField(label="Kleur onder", required=False)

    class Meta:
        model = UserSetting
        fields = '__all__'

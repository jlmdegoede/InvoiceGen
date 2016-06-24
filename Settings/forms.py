from django import forms
from django.contrib.auth.models import User
from django import forms
from Settings.models import UserSetting
from colorful.forms import RGBColorField


class UserSettingForm(forms.ModelForm):
    site_name = forms.CharField(label="Websitenaam", max_length=200)
    kvk = forms.CharField(label="Websitenaam", required=False)
    btw_number = forms.CharField(label="Websitenaam", required=False)

    class Meta:
        model = UserSetting
        fields = '__all__'


class ColorForm(forms.Form):
    color_down = RGBColorField()
    color_up = RGBColorField()

from django import forms
from django.contrib.auth.models import User
from django import forms
from Settings.models import UserSetting
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class UserSettingForm(forms.ModelForm):
    site_name = forms.CharField(label="Websitenaam", max_length=200)
    kvk = forms.CharField(label="Websitenaam", required=False)
    btw_number = forms.CharField(label="Websitenaam", required=False)
    color_up = forms.CharField(label="Kleur boven", required=False)
    color_down = forms.CharField(label="Kleur onder", required=False)

    class Meta:
        model = UserSetting
        fields = '__all__'

class UserForm(forms.ModelForm):
    username = forms.CharField(label="Gebruikersnaam", max_length=100)
    email = forms.EmailField(label="E-mailadres")
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ('username', 'email', 'groups')

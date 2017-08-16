from django import forms
from django.contrib.auth.models import User
from django import forms
from settings.models import UserSetting
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class UserSettingForm(forms.ModelForm):

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

from django import forms
from django.contrib.auth.models import User
from django import forms
from Company.models import *
from datetime import date


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = '__all__'
from django import forms
from django.contrib.auth.models import User
from django import forms
from orders.models import *
from datetime import date


class UserForm(forms.ModelForm):
    password = forms.CharField(label="Wachtwoord", widget=forms.PasswordInput())
    username = forms.CharField(label="E-mailadres")
    username.help_text = ""

    class Meta:
        model = User
        fields = ('username', 'password')


class ProductForm(forms.ModelForm):
    title = forms.CharField(label="Titel", max_length=200)
    date_received = forms.DateField(label="Ontvangen op", input_formats=['%d-%m-%Y'], initial=date.today(), widget=forms.widgets.DateInput(format="%d-%m-%Y",attrs={'class':'datepicker'}))
    date_deadline = forms.DateField(label="Deadline", input_formats=['%d-%m-%Y'], widget=forms.widgets.DateInput(format="%d-%m-%Y",attrs={'class':'datepicker'}))
    quantity = forms.IntegerField(label="Aantal")
    from_company = forms.ModelChoiceField(queryset=Company.objects.all(), required=False, widget=forms.Select())
    identification_number = forms.CharField(label="Volgnummer", required=False)
    price_per_quantity = forms.DecimalField(label="Prijs per product")
    briefing = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea'}), required=False)
    done = forms.BooleanField(label="Klaar", required=False)
    tax_rate = forms.IntegerField(label="BTW-tarief", required=False)

    class Meta:
        model = Product
        fields = ('title', 'date_received', 'date_deadline', 'quantity', 'from_company', 'identification_number', 'tax_rate', 'price_per_quantity', 'briefing', 'done')


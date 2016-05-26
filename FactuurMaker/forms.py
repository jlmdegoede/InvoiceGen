from django import forms
from django.contrib.auth.models import User
from django import forms
from FactuurMaker.models import *
from datetime import date


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField()
    username.help_text = ""

    class Meta:
        model = User
        fields = ('username', 'password')


class ProductForm(forms.ModelForm):
    title = forms.CharField(label="Titel", max_length=200)
    date_received = forms.DateField(label="Ontvangen op", input_formats=['%d-%m-%Y'], initial=date.today(), widget=forms.widgets.DateInput(format="%d-%m-%Y",attrs={'class':'datepicker'}))
    date_deadline = forms.DateField(label="Deadline", input_formats=['%d-%m-%Y'], widget=forms.widgets.DateInput(format="%d-%m-%Y",attrs={'class':'datepicker'}))
    quantity = forms.IntegerField(label="Aantal")
    from_company = forms.CharField(label="Bedrijf", max_length=200)
    identification_number = forms.IntegerField(label="Volgnummer")
    price_per_quantity = forms.DecimalField(label="Prijs per product")
    briefing = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea'}), required=False)
    done = forms.BooleanField(label="Klaar", required=False)

    class Meta:
        model = Product
        fields = ('title', 'date_received', 'date_deadline', 'quantity', 'from_company', 'identification_number', 'price_per_quantity', 'briefing', 'done')


class InvoiceForm(forms.ModelForm):
    date_created = forms.DateField(label="Aangemaakt op", input_formats=['%d-%m-%Y'], initial=date.today(), widget=forms.widgets.DateInput(format="%d-%m-%Y",attrs={'class':'datepicker'}))
    to_address = forms.CharField(label="Aan", max_length=200)
    from_address = forms.CharField(label="Van", max_length=200)
    file_path = forms.CharField(label="Bestand", max_length=200)
    invoice_number = forms.IntegerField(label="Volgnummer")
    total_amount = forms.IntegerField(label="Totaalbedrag")
    articles = forms.ModelMultipleChoiceField(queryset=Product.objects.all())

    class Meta:
        model = Invoice
        fields = '__all__'


class UserSettingForm(forms.ModelForm):

    class Meta:
        model = UserSetting
        fields = '__all__'


class CompanySettingForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = '__all__'
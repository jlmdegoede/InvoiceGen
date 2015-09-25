from django import forms
from django.contrib.auth.models import User
from django import forms
from FactuurMaker.models import *
from datetime import date

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class ArticleForm(forms.ModelForm):
    title = forms.CharField(label="Titel", max_length=200)
    date_received = forms.DateField(label="Ontvangen op", input_formats=['%d-%m-%Y'], initial=date.today(), widget=forms.widgets.DateInput(format="%d-%m-%Y",attrs={'class':'datepicker'}))
    date_deadline = forms.DateField(label="Deadline", input_formats=['%d-%m-%Y'], widget=forms.widgets.DateInput(format="%d-%m-%Y",attrs={'class':'datepicker'}))
    word_count = forms.IntegerField(label="Woordenaantal")
    magazine = forms.CharField(label="Magazine", max_length=200)
    magazine_number = forms.IntegerField(label="Magazinenummer")
    word_price = forms.DecimalField(label="Woordprijs")
    briefing = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea'}), required=False)
    paid = forms.BooleanField(label="Betaald", required=False)
    done = forms.BooleanField(label="Klaar", required=False)

    class Meta:
        model = Article
        fields = ('title', 'date_received', 'date_deadline', 'word_count', 'magazine', 'magazine_number', 'word_price', 'briefing', 'paid', 'done')

class InvoiceForm(forms.ModelForm):
    date_created = forms.DateField(label="Aangemaakt op", input_formats=['%d-%m-%Y'], initial=date.today(), widget=forms.widgets.DateInput(format="%d-%m-%Y",attrs={'class':'datepicker'}))
    to_address = forms.CharField(label="Aan", max_length=200)
    from_address = forms.CharField(label="Van", max_length=200)
    file_path = forms.CharField(label="Bestand", max_length=200)
    invoice_number = forms.IntegerField(label="Volgnummer")
    total_amount = forms.IntegerField(label="Totaalbedrag")
    articles = forms.ModelMultipleChoiceField(queryset=Article.objects.all())

    class Meta:
        model = Invoice
        fields = '__all__'

class UserSettingForm(forms.ModelForm):

    class Meta:
        model = UserSetting
        fields = '__all__'

class CompanySettingForm(forms.ModelForm):

    class Meta:
        model = CompanySetting
        fields = '__all__'
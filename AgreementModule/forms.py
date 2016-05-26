from django import forms
from FactuurMaker.models import *
import datetime
from AgreementModule.models import AgreementText, Agreement


class AgreementTextForm(forms.ModelForm):
    title = forms.CharField(label="Titel", max_length=200)
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea'}), required=False)

    class Meta:
        model = Product
        fields = ('title', 'text',)


class AgreementForm(forms.ModelForm):
    agree_text = forms.ModelChoiceField(queryset=AgreementText.objects.all(), widget=forms.Select())
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.Select())
    article_concerned = forms.ModelMultipleChoiceField(queryset=Product.objects.all())
    client_name = forms.CharField(label="Naam opdrachtgever", max_length=200)
    client_emailaddress = forms.CharField(label="E-mailadres opdrachtgever", max_length=200)

    class Meta:
        model = Agreement
        fields = ('agree_text', 'article_concerned', 'client_name', 'client_emailaddress')
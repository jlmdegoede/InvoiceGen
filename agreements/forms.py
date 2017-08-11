from django import forms

from markdownx.fields import MarkdownxFormField

from orders.models import *

from .models import Agreement, AgreementText, AgreementTextVariable


class AgreementTextVariableForm(forms.ModelForm):
    name = forms.CharField(label="Naam", max_length=200)
    description = forms.CharField(label="Omschrijving", max_length=200)


class AgreementTextForm(forms.ModelForm):
    title = forms.CharField(label="Titel", max_length=200)
    text = MarkdownxFormField()
    variables = forms.ModelMultipleChoiceField(queryset=AgreementTextVariable.objects.all(), required=False)

    class Meta:
        model = AgreementText
        fields = ('title', 'text', 'variables')


class AgreementForm(forms.ModelForm):
    agreement_text = forms.ModelChoiceField(queryset=AgreementText.objects.all(), widget=forms.Select())
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.Select())
    article_concerned = forms.ModelMultipleChoiceField(queryset=Product.objects.all())
    client_name = forms.CharField(label="Naam opdrachtgever", max_length=200)
    client_emailaddress = forms.CharField(label="E-mailadres opdrachtgever", max_length=200,
                                          widget=forms.TextInput(attrs={'class': 'validate', 'type': 'email'}))

    class Meta:
        model = Agreement
        fields = ('agreement_text', 'article_concerned', 'client_name', 'client_emailaddress')


class SignatureForm(forms.Form):
    signature = forms.FileField(required=True)
    signee_name = forms.CharField(label="Naam", required=True)

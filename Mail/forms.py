from django import forms
from .models import Email, EmailTemplate

class EmailForm(forms.ModelForm):
    subject = forms.CharField(label="Onderwerp", max_length=200)
    to = forms.EmailField(label="Aan", max_length=200)
    cc = forms.EmailField(label="CC", max_length=200, required=False)
    bcc = forms.EmailField(label="BCC", max_length=200, required=False)
    contents = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea'}))
    attach_pdf = forms.BooleanField(label="Voeg PDF als bijlage toe", required=False)

    class Meta:
        model = Email
        fields = '__all__'

class EmailTemplateForm(forms.ModelForm):
    subject = forms.CharField(label="Onderwerp", max_length=200)
    contents = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea'}))

    class Meta:
        model = EmailTemplate
        fields = ('subject', 'contents')

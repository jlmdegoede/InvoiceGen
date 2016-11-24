from django import forms

class EmailForm(forms.Form):
    subject = forms.CharField(label="Onderwerp", max_length=200)
    to = forms.CharField(label="Aan", max_length=200)
    cc = forms.CharField(label="CC", max_length=200, required=False)
    bcc = forms.CharField(label="BCC", max_length=200, required=False)
    contents = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea'}))
    attach_pdf = forms.BooleanField(label="Voeg PDF als bijlage toe", required=False)

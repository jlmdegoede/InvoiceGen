from django import forms
from Orders.models import *


class InvoiceForm(forms.ModelForm):
    title = forms.CharField(label="Titel", max_length=200)
    invoice_number = forms.IntegerField(label="Volgnummer")
    articles = forms.ModelMultipleChoiceField(queryset=Product.objects.all())
    paid = forms.BooleanField(label="Betaald", required=False)
    expiration_date = forms.DateField(label="Vervaldatum", input_formats=['%d-%m-%Y'], widget=forms.widgets.DateInput(format="%d-%m-%Y",attrs={'class':'datepicker'}))

    class Meta:
        model = Invoice
        fields = ('invoice_number', 'paid', 'title', 'expiration_date')
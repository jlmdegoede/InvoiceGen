from django import forms

from orders.models import *


class OutgoingInvoiceForm(forms.ModelForm):
    title = forms.CharField(label="Titel", max_length=200)
    invoice_number = forms.IntegerField(label="Volgnummer")
    paid = forms.BooleanField(label="Betaald", required=False)
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())
    expiration_date = forms.DateField(label="Vervaldatum", input_formats=['%d-%m-%Y'], widget=forms.widgets.DateInput(format="%d-%m-%Y",attrs={'class':'datepicker'}))

    class Meta:
        model = OutgoingInvoice
        fields = ('invoice_number', 'paid', 'title', 'expiration_date')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(OutgoingInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['products'].initial = [c.pk for c in Product.objects.filter(invoice=instance.pk)]


class IncomingInvoiceForm(forms.ModelForm):
    title = forms.CharField(label="Titel", max_length=200)
    invoice_number = forms.CharField(label="Volgnummer")
    paid = forms.BooleanField(label="Betaald", required=False)
    received_date = forms.DateField(label="Vervaldatum", input_formats=['%d-%m-%Y'], widget=forms.widgets.DateInput(format="%d-%m-%Y",attrs={'class':'datepicker'}))
    invoice_file = forms.FileField(required=False)
    subtotal = forms.DecimalField(decimal_places=2)
    btw_amount = forms.DecimalField(decimal_places=2)

    class Meta:
        model = OutgoingInvoice
        fields = ('invoice_number', 'paid', 'title', 'invoice_file', 'received_date', 'subtotal', 'btw_amount')

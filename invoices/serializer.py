from rest_framework import serializers

from .models import OutgoingInvoice


class OutgoingInvoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OutgoingInvoice
        fields = ('title', 'date_created', 'invoice_number', 'paid', 'to_company', 'expiration_date', 'url')

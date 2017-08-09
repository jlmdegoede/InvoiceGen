from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'date_received', 'date_deadline', 'from_company', 'quantity', 'identification_number', 'invoice',
                  'briefing', 'done', 'price_per_quantity', 'tax_rate')

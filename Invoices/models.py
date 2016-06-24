from Companies.models import *
from django.core.exceptions import ValidationError


class Invoice(models.Model):
    title = models.CharField(max_length=200)
    date_created = models.DateField()
    invoice_number = models.IntegerField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    class Meta:
        abstract = True


class OutgoingInvoice(Invoice):
    total_amount = models.IntegerField()
    to_company = models.ForeignKey(to=Company)
    expiration_date = models.DateField()

    def get_totaalbedrag(self):
        from Orders.models import Product
        totaalbedrag = 0
        products = Product.objects.filter(invoice=self)
        for product in products:
            totaalbedrag += product.get_price()
        return totaalbedrag

    def get_btw(self):
        from Orders.models import Product
        btw = 0
        products = Product.objects.filter(invoice=self)
        for product in products:
            btw += product.get_price() * (float(product.tax_rate / 100))
        return btw


class IncomingInvoice(Invoice):
    def generate_filename(self, filename):
        url = "invoices/%s/%s" % (self.in_or_outgoing, filename)
        return url

    def validate_file_extension(value):
        if value.file.content_type != 'application/pdf':
            raise ValidationError(u'Error message')

    invoice_file = models.FileField(upload_to=generate_filename, null=True, validators=[validate_file_extension])
    received_date = models.DateField()
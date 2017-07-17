from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from companies.models import *
from InvoiceGen.site_settings import ALLOWED_HOSTS


class Invoice(models.Model):
    title = models.CharField(max_length=200)
    date_created = models.DateField()
    invoice_number = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        permissions = (
            ('view_invoice', 'Kan factuur bekijken'),
        )


class OutgoingInvoice(Invoice):
    to_company = models.ForeignKey(to=Company)
    expiration_date = models.DateField()
    url = models.CharField(max_length=32, null=True)

    def get_total_amount(self):
        from orders.models import Product
        totaalbedrag = 0
        products = Product.objects.filter(invoice=self)
        for product in products:
            totaalbedrag += product.get_price()
        return totaalbedrag

    def get_total_amount_including_btw(self):
        return self.get_total_amount() + self.get_btw()

    def get_btw(self):
        from orders.models import Product
        btw = 0
        products = Product.objects.filter(invoice=self)
        for product in products:
            btw += product.get_price() * (float(product.tax_rate / 100))
        return btw

    def get_complete_url(self):
        if self.url is not None:
            return 'https://{0}{1}'.format(ALLOWED_HOSTS[0], reverse('view_outgoing_invoice_guest', args=[self.url]))


class IncomingInvoice(Invoice):
    def generate_filename(self, filename):
        url = "invoices/%s/%s" % (self.in_or_outgoing, filename)
        return url

    def validate_file_extension(value):
        try:
            if value and value.file and value.file.content_type != 'application/pdf':
                raise ValidationError(u'Alleen PDF-bestanden toegestaan')
        except:
            print("Geen contenttype gevonden")

    @property
    def pdf_url(self):
        if self.invoice_file and hasattr(self.invoice_file, 'url'):
            return self.invoice_file.url

    subtotal = models.DecimalField(decimal_places=2, max_digits=100)
    btw_amount = models.DecimalField(decimal_places=2, max_digits=100)
    invoice_file = models.FileField(upload_to='invoice-pdfs/%Y/%m/%d', null=True, validators=[validate_file_extension])
    received_date = models.DateField()

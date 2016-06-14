from Companies.models import *

class Invoice(models.Model):
    title = models.CharField(max_length=200)
    date_created = models.DateField()
    to_company = models.ForeignKey(to=Company)
    contents = models.TextField()
    invoice_number = models.IntegerField()
    total_amount = models.IntegerField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.title

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

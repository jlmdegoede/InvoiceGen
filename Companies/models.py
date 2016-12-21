from django.db import models


class Company(models.Model):
    company_name = models.CharField(max_length=200)
    company_address = models.CharField(max_length=200)
    company_city_and_zipcode = models.CharField(max_length=200)
    company_email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.company_name

    class Meta:
        permissions = (
            ('view_company', 'Kan opdrachtgever bekijken'),
        )

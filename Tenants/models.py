from django.db import models
from tenant_schemas.models import TenantMixin
from datetime import datetime, timedelta

class Client(TenantMixin):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    subdomain = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    customer_number = models.IntegerField()
    valid_until = models.DateTimeField(default=datetime.now()+timedelta(days=31))
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.subdomain

    def get_complete_url(self, url):
        return 'https://' + self.subdomain + '.invoicegen.nl' + url

    def add_days_to_subscription(self, days):
        now = timezone.now()
        if now > self.valid_until:
            self.valid_until = timezone.now() + timedelta(days=days)
        else:
            self.valid_until = self.valid_until + timedelta(days=days)
        self.save()

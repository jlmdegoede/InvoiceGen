from django.contrib import admin
from .models import InvoiceTemplate


class InvoiceTemplateAdmin(admin.ModelAdmin):
    pass
admin.site.register(InvoiceTemplate, InvoiceTemplateAdmin)
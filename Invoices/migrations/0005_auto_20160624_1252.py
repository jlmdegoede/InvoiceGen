# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-24 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoices', '0004_auto_20160624_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incominginvoice',
            name='btw_amount',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
        migrations.AlterField(
            model_name='incominginvoice',
            name='invoice_number',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='incominginvoice',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
        migrations.AlterField(
            model_name='outgoinginvoice',
            name='invoice_number',
            field=models.CharField(max_length=100),
        ),
    ]

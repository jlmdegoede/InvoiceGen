# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0003_product_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='identification_number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
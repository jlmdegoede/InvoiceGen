# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 09:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tenants', '0003_auto_20170201_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='valid_until',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 4, 10, 43, 19, 435737)),
        ),
    ]

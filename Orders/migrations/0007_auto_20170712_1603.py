# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-12 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0006_auto_20161125_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='briefing',
            field=models.TextField(null=True),
        ),
    ]

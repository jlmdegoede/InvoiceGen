# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-24 11:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='invoice',
        ),
    ]
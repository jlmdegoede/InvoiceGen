# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0006_auto_20150412_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date_sent',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]

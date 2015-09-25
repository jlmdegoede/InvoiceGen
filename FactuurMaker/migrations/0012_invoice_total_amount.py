# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0011_auto_20150420_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='total_amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

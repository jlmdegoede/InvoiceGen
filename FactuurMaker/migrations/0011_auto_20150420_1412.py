# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0010_auto_20150413_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='done',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0003_auto_20150409_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='invoice',
            field=models.ForeignKey(blank=True, to='FactuurMaker.Invoice', null=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0015_auto_20150729_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='word_price',
            field=models.FloatField(default=0.25),
        ),
    ]

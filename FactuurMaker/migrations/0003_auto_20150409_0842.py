# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0002_article_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='paid',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

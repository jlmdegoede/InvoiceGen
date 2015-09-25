# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0005_article_briefing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date_sent',
            field=models.DateField(blank=True),
            preserve_default=True,
        ),
    ]

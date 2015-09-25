# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0004_auto_20150409_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='briefing',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]

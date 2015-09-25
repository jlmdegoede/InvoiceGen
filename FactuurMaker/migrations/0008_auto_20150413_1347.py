# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0007_auto_20150412_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='date_sent',
        ),
        migrations.AddField(
            model_name='invoice',
            name='file_path',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

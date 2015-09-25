# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0013_auto_20150422_1053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='date',
            new_name='date_received',
        ),
    ]

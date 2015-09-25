# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0014_auto_20150422_1056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='file_path',
            new_name='contents',
        ),
    ]

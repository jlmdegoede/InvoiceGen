# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0012_invoice_total_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='date_received',
            new_name='date',
        ),
    ]

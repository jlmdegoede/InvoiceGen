# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0017_magazine_magazineuitgave'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='magazineuitgave',
            name='magazine',
        ),
        migrations.DeleteModel(
            name='Magazine',
        ),
        migrations.DeleteModel(
            name='MagazineUitgave',
        ),
    ]

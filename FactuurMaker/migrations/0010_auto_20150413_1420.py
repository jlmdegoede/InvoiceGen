# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0009_setting'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanySetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bedrijfsnaam', models.CharField(max_length=200)),
                ('bedrijfsadres', models.CharField(max_length=200)),
                ('bedrijfsplaats', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('naam', models.CharField(max_length=200)),
                ('adres', models.CharField(max_length=200)),
                ('woonplaats', models.CharField(max_length=200)),
                ('emailadres', models.CharField(max_length=200)),
                ('iban', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Setting',
        ),
    ]

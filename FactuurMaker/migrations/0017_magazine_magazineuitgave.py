# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FactuurMaker', '0016_article_word_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titel', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MagazineUitgave',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nummer', models.CharField(max_length=10)),
                ('verschijningsdatum', models.DateField()),
                ('magazine', models.ForeignKey(to='FactuurMaker.Magazine')),
            ],
        ),
    ]

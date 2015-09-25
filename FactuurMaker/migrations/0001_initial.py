# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('date_received', models.DateField()),
                ('date_deadline', models.DateField()),
                ('word_count', models.IntegerField()),
                ('magazine', models.CharField(max_length=40)),
                ('magazine_number', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateField()),
                ('date_sent', models.DateField()),
                ('to_address', models.TextField(default=b'')),
                ('from_address', models.TextField(default=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='invoice',
            field=models.ForeignKey(to='FactuurMaker.Invoice', blank=True),
            preserve_default=True,
        ),
    ]

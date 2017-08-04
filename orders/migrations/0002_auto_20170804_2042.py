# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('attachment', models.FileField(upload_to='attachments/')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='attachments',
            field=models.ManyToManyField(to='orders.ProductAttachment'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 09:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Invoices', '0001_initial'),
        ('Companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date_received', models.DateField()),
                ('date_deadline', models.DateField()),
                ('quantity', models.IntegerField()),
                ('identification_number', models.IntegerField(null=True)),
                ('briefing', models.TextField(blank=True)),
                ('done', models.BooleanField(default=False)),
                ('price_per_quantity', models.FloatField()),
                ('tax_rate', models.IntegerField()),
                ('from_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Companies.Company')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Invoices.Invoice')),
            ],
        ),
    ]

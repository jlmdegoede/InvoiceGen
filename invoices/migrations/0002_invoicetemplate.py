# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-09 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('main_file', models.CharField(max_length=100)),
                ('order_template', models.TextField(blank=True)),
                ('template_type', models.CharField(choices=[('docx', 'DOCX'), ('latex', 'LaTeX'), ('md', 'Markdown')], max_length=10)),
                ('preview_image', models.ImageField(upload_to='images/')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-24 17:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('FactuurMaker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signed_by_client', models.BooleanField(default=False)),
                ('signed_by_client_at', models.DateTimeField(null=True)),
                ('client_name', models.CharField(max_length=200)),
                ('client_emailaddress', models.CharField(max_length=200)),
                ('agreement_text_copy', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AgreementText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('text', models.TextField()),
                ('edited_at', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='agreement',
            name='agree_text',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AgreementModule.AgreementText'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='article_concerned',
            field=models.ManyToManyField(to='FactuurMaker.Product'),
        ),
    ]

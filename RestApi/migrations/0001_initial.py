# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionIDs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_token', models.CharField(max_length=700)),
                ('session_id', models.CharField(max_length=200)),
                ('date_created', models.DateField()),
                ('valid', models.BooleanField()),
                ('device', models.CharField(max_length=100)),
                ('software_version', models.CharField(max_length=10)),
                ('last_known_ip', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

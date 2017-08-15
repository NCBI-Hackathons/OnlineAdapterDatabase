# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 15:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oadb', '0004_auto_20170815_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='adaptor',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

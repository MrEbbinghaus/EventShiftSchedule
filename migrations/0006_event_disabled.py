# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-07 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventShiftSchedule', '0005_auto_20160928_0710'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]

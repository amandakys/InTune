# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intune', '0016_auto_20170609_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='unread_notifications',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

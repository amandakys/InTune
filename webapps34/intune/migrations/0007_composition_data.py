# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intune', '0006_delete_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='data',
            field=models.CharField(blank=True, max_length=10000),
        ),
    ]
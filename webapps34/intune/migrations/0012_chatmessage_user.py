# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 02:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intune', '0011_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='intune.Profile'),
            preserve_default=False,
        ),
    ]

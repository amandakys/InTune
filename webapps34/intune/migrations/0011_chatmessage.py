# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-08 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intune', '0010_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.CharField(max_length=200)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room', to='intune.Room')),
            ],
        ),
    ]

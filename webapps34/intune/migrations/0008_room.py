# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 15:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intune', '0007_composition_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('composition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='composition', to='intune.Composition')),
            ],
        ),
    ]

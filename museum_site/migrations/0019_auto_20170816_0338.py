# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-16 03:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_site', '0018_auto_20170816_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='playable_boards',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='total_boards',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]

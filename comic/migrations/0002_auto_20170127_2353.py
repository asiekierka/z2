# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-27 23:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comic',
            options={'ordering': ['comic_id']},
        ),
        migrations.RenameField(
            model_name='comic',
            old_name='stripcreator_account',
            new_name='comic_account',
        ),
        migrations.RenameField(
            model_name='comic',
            old_name='stripcreator_id',
            new_name='comic_id',
        ),
    ]

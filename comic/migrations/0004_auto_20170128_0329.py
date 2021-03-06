# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-28 03:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0003_auto_20170128_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='comic_account',
            field=models.CharField(choices=[('benco', 'Benco'), ('bencomic', 'Bencomic'), ('lemmy', 'Lemmy'), ('mr-shapiro', 'Mr. Shapiro'), ('nomad', "Nomad's ZZT Comics"), ('kaddar', 'Yellow Boarders'), ('frost', 'Frost'), ('revvy', 'The Prophesies of Revvy'), ('zamros', 'Zamros: The Comic'), ('ubgs', "Ol' Uncle Bo's Gamblin' Shack")], max_length=10),
        ),
        migrations.AlterField(
            model_name='comic',
            name='transcript',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]

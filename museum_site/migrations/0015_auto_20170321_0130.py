# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-21 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_site', '0014_auto_20170307_2316'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'ordering': ['sort_title', 'letter']},
        ),
        migrations.AlterField(
            model_name='article',
            name='type',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='file',
            name='category',
            field=models.CharField(choices=[('?', '?'), ('MS-DOS', 'MS-DOS Programs'), ('WIN16', '16-Bit Windows Programs'), ('WIN32', '32-Bit Windows Programs'), ('WIN64', '64-Bit Windows Programs'), ('LINUX', 'Linux Programs'), ('OSX', 'OSX Programs'), ('FEATURED', 'Featured Worlds'), ('CONTEST', 'Contest Entries'), ('ZZM', 'ZZM Soundtrack'), ('GFX', 'Modified Graphics'), ('MOD', 'Modified Executables'), ('ETC', 'Etc.'), ('SZZT', 'Super ZZT Worlds'), ('UTILITY', 'Utilities'), ('ZZT', 'ZZT Worlds'), ('ZIG', 'ZIG World'), ('LOST', 'Lost Worlds'), ('UPLOADED', 'Uploaded Worlds'), ('REMOVED', 'Removed Worlds')], max_length=10),
        ),
        migrations.AlterField(
            model_name='file',
            name='sort_title',
            field=models.CharField(blank=True, db_index=True, default='', help_text='Leave blank to set automatically', max_length=100),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-03 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0010_auto_20170703_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keywordgroup',
            name='group_name',
            field=models.CharField(db_index=True, max_length=20, unique=True, verbose_name='组名'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-23 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0004_auto_20170623_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='web_count',
            field=models.IntegerField(default=1, verbose_name='出现网站个数'),
        ),
    ]

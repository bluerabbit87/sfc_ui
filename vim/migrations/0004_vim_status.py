# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 07:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vim', '0003_auto_20160510_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='vim',
            name='status',
            field=models.CharField(default='unknown', max_length=50),
        ),
    ]
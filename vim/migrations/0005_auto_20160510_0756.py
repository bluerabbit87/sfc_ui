# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vim', '0004_vim_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vim',
            name='status',
            field=models.CharField(default='unknown', max_length=100),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdn_controllers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sdncontroller',
            old_name='status',
            new_name='health',
        ),
        migrations.AddField(
            model_name='sdncontroller',
            name='memory',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='sdncontroller',
            name='tables',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='sdncontroller',
            name='uptime',
            field=models.CharField(default='unknown', max_length=50),
        ),
    ]

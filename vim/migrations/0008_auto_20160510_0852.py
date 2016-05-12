# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vim', '0007_auto_20160510_0840'),
    ]

    operations = [
        migrations.RenameField(
            model_name='port',
            old_name='binding',
            new_name='binding_host_id',
        ),
        migrations.AddField(
            model_name='port',
            name='binding_vnic_type',
            field=models.CharField(default='unknown', max_length=50),
        ),
    ]
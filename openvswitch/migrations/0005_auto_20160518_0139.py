# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 01:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('openvswitch', '0004_auto_20160518_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ovsbridge',
            name='controller',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='openvswitch.OVSController'),
        ),
    ]

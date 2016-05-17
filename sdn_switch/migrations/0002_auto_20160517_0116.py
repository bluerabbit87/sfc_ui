# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 01:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sdn_switch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controller',
            name='owner_controller',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sdn_controllers.SDNController'),
        ),
        migrations.AlterField(
            model_name='host',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='openvswitch',
            name='_uuid',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='openvswitch',
            name='owner_Host',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sdn_switch.Host'),
        ),
        migrations.AlterField(
            model_name='ovsbridge',
            name='controller',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sdn_controllers.SDNController'),
        ),
        migrations.AlterField(
            model_name='ovsbridge',
            name='owner_Host',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sdn_switch.Host'),
        ),
        migrations.AlterField(
            model_name='ovsinterface',
            name='owner_host',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sdn_switch.Host'),
        ),
        migrations.AlterField(
            model_name='ovsport',
            name='owner_Bridge',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sdn_switch.OVSBridge'),
        ),
    ]

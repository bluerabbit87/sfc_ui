# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 06:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sdn_switch', '0002_controller_ovsbridge_ovsinterface_ovsport'),
    ]

    operations = [
        migrations.CreateModel(
            name='SDNController',
            fields=[
                ('id', models.AutoField(default=None, primary_key=True, serialize=False)),
                ('mgmt_ip', models.CharField(default='unknown', max_length=50)),
                ('mgmt_port', models.CharField(default='unknown', max_length=50)),
                ('status', models.CharField(default='unknown', max_length=50)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdn_switch.Host')),
            ],
        ),
    ]

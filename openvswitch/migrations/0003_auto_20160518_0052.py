# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 00:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('openstack', '0001_initial'),
        ('floodlight', '0006_auto_20160517_0606'),
        ('openvswitch', '0002_auto_20160517_0116'),
    ]

    operations = [
        migrations.CreateModel(
            name='OVSController',
            fields=[
                ('_uuid', models.CharField(default='unknown', max_length=50, primary_key=True, serialize=False)),
                ('connection_mode', models.CharField(default='unknown', max_length=50)),
                ('controller_burst_limit', models.CharField(default='unknown', max_length=50)),
                ('controller_rate_limit', models.CharField(default='unknown', max_length=50)),
                ('enable_async_messages', models.CharField(default='unknown', max_length=50)),
                ('external_ids', models.CharField(default='unknown', max_length=50)),
                ('inactivity_probe', models.CharField(default='unknown', max_length=50)),
                ('is_connected', models.CharField(default='unknown', max_length=50)),
                ('local_gateway', models.CharField(default='unknown', max_length=50)),
                ('local_ip', models.CharField(default='unknown', max_length=50)),
                ('local_netmask', models.CharField(default='unknown', max_length=50)),
                ('max_backoff', models.CharField(default='unknown', max_length=50)),
                ('other_config', models.CharField(default='unknown', max_length=50)),
                ('role', models.CharField(default='unknown', max_length=50)),
                ('status', models.CharField(default='unknown', max_length=50)),
                ('target', models.CharField(default='unknown', max_length=50)),
                ('owner_controller', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='floodlight.SDNController')),
            ],
        ),
        migrations.RemoveField(
            model_name='controller',
            name='owner_controller',
        ),
        migrations.RemoveField(
            model_name='host',
            name='hypervisor',
        ),
        migrations.RemoveField(
            model_name='openvswitch',
            name='owner_Host',
        ),
        migrations.RemoveField(
            model_name='ovsbridge',
            name='owner_Host',
        ),
        migrations.RemoveField(
            model_name='ovsinterface',
            name='owner_host',
        ),
        migrations.AddField(
            model_name='openvswitch',
            name='hypervisor',
            field=models.ForeignKey(default='unknown', on_delete=django.db.models.deletion.CASCADE, to='openstack.Hypervisor'),
        ),
        migrations.AddField(
            model_name='openvswitch',
            name='mgmt_id',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='openvswitch',
            name='mgmt_ip',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='openvswitch',
            name='mgmt_password',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='openvswitch',
            name='mgmt_port',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='openvswitch',
            name='status',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='ovsbridge',
            name='owner_ovs',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='openvswitch.OpenvSwitch'),
        ),
        migrations.AddField(
            model_name='ovsinterface',
            name='owner_ovs',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='openvswitch.OpenvSwitch'),
        ),
        migrations.AddField(
            model_name='ovsport',
            name='owner_ovs',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='openvswitch.OpenvSwitch'),
        ),
        migrations.DeleteModel(
            name='Controller',
        ),
        migrations.DeleteModel(
            name='Host',
        ),
        migrations.AddField(
            model_name='ovscontroller',
            name='owner_ovs',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='openvswitch.OpenvSwitch'),
        ),
    ]

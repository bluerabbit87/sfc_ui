# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 09:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('openstack', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vim',
            old_name='user_domain_id',
            new_name='user_domain_name',
        ),
    ]
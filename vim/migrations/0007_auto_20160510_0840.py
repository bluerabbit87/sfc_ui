# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 08:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vim', '0006_port'),
    ]

    operations = [
        migrations.RenameField(
            model_name='port',
            old_name='parent_vim',
            new_name='owner_vim',
        ),
    ]

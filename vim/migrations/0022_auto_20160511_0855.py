# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-11 08:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vim', '0021_auto_20160511_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hypervisor',
            name='owner_vim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vim.VIM'),
        ),
        migrations.AlterField(
            model_name='network',
            name='owner_vim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vim.VIM'),
        ),
        migrations.AlterField(
            model_name='port',
            name='owner_vim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vim.VIM'),
        ),
        migrations.AlterField(
            model_name='server',
            name='owner_vim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vim.VIM'),
        ),
    ]
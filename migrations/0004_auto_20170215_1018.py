# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 10:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20170215_0931'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='result',
            new_name='balance',
        ),
    ]

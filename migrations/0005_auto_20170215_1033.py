# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 10:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20170215_1018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='expenses_text',
            new_name='expenses',
        ),
        migrations.RenameField(
            model_name='account',
            old_name='income_text',
            new_name='income',
        ),
    ]

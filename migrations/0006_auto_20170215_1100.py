# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20170215_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='save_date',
            field=models.CharField(max_length=10),
        ),
    ]

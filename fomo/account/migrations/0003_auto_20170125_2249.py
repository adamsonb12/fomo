# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 22:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170125_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fomouser',
            name='birth_date',
            field=models.DateField(null=True),
        ),
    ]

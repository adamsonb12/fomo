# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-08 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_saleitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]

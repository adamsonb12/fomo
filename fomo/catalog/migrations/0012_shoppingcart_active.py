# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-08 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_shoppingcart_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
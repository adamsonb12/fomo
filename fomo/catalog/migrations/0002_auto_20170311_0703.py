# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-11 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='descriptionList',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='imgList',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='codename',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]
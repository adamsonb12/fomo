# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 01:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20170328_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalproduct',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='rentalproduct',
            name='sold',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sale',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='sale',
            name='total_tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='saleitems', to='catalog.Product'),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=7.25, max_digits=8),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='tax_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='uniqueproduct',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='uniqueproduct',
            name='sold',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='catalog.Sale'),
        ),
        migrations.AlterField(
            model_name='producthistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale', to='catalog.Sale'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Product'),
        ),
    ]

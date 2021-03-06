# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-24 06:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_sales_truck_route'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales',
            old_name='money_made',
            new_name='revenue',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='date_updated',
        ),
        migrations.AddField(
            model_name='sales',
            name='quantity_sold',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='sales',
            name='date_added',
            field=models.DateTimeField(),
        ),
    ]

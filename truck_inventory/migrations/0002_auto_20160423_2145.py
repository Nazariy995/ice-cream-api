# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-23 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truck_inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='truckinventory',
            name='date_added',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='truckinventory',
            name='item_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='truckinventory',
            name='truck_number',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='truckinventory',
            unique_together=set([('truck_number', 'item_number', 'date_added')]),
        ),
    ]
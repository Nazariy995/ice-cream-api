# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-25 01:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truck_inventory', '0002_auto_20160423_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='truckinventory',
            name='description',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
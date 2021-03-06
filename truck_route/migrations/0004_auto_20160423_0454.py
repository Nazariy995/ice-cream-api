# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-23 04:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('truck_route', '0003_auto_20160423_0347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='truckroute',
            old_name='route_number',
            new_name='route',
        ),
        migrations.RenameField(
            model_name='truckroute',
            old_name='truck_number',
            new_name='truck',
        ),
        migrations.AlterUniqueTogether(
            name='truckroute',
            unique_together=set([('truck', 'route', 'date_added')]),
        ),
    ]

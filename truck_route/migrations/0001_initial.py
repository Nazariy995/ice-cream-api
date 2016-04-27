# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-08 00:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trucks', '0002_auto_20160406_0147'),
        ('routes', '0002_auto_20160406_0107'),
    ]

    operations = [
        migrations.CreateModel(
            name='TruckRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('route_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routes.Route')),
                ('truck_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trucks.Truck')),
            ],
        ),
    ]

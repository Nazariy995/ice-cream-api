# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-06 01:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('routes', '0002_auto_20160406_0107'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_label', models.CharField(max_length=100)),
                ('city_name', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=2)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routes.Route')),
            ],
        ),
    ]

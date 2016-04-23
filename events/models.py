from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Event(models.Model):
    city = models.CharField(max_length=100)
    date = models.DateField()
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('city', 'date', 'name')

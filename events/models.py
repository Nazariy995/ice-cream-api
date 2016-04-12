from __future__ import unicode_literals

from django.db import models
from cites.models import City

# Create your models here.

class Events(models.Model):
    city_label = models.ForeignKey(City, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    event_name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
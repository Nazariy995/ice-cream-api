from __future__ import unicode_literals

from django.db import models
from routes.models import Route

# Create your models here.
class City(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True)
    city_label = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    state = models.CharField(max_length=2)

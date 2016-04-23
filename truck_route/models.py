from __future__ import unicode_literals

from django.db import models
from trucks.models import Truck
from routes.models import Route

# Create your models here.

class TruckRoute(models.Model):
    truck_number = models.IntegerField()
    route_number = models.IntegerField()
    date_added = models.DateField(null=True)

    class Meta:
        unique_together = ('truck_number', 'route_number', 'date_added')


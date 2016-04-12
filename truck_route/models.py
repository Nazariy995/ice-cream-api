from __future__ import unicode_literals

from django.db import models
from trucks.models import Truck
from routes.models import Route

# Create your models here.

class TruckRoute(models.Model):
    truck_number = models.ForeignKey(Truck, on_delete=models.CASCADE)
    route_number = models.ForeignKey(Route, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add= True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)
    
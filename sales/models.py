from __future__ import unicode_literals

from django.db import models
from truck_route.models import TruckRoute
from datetime import date
from django.utils import timezone

# Create your models here.

class Sales(models.Model):
    truck_route = models.ForeignKey(TruckRoute)
    revenue = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_sold = models.IntegerField(null=True)
    date_added = models.DateField(null=False)

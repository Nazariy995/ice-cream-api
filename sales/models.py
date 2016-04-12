from __future__ import unicode_literals

from django.db import models
from truck_route.models import TruckRoute

# Create your models here.

class Sales(models.Model):
    truck_route = models.ForeignKey(TruckRoute)
    money_made = models.DecimalField(max_digits=8, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add= True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)
    
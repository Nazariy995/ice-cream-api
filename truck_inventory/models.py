from __future__ import unicode_literals

from django.db import models
from trucks.models import Truck

# Create your models here.

class TruckInventory(models.Model):
    truck_number = models.IntegerField()
    item_number = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    description = models.CharField(max_length=250, null=True)
    date_added = models.DateField(null=True, auto_now_add=True)

    class Meta:
        unique_together = ('truck_number', 'item_number', 'date_added')

from __future__ import unicode_literals

from django.db import models
from trucks.models import Truck
from warehouse_inventory.models import WarehouseInventory

# Create your models here.

class TruckInventory(models.Model):
    truck_number = models.ForeignKey(Truck, on_delete=models.CASCADE)
    item_number = models.ForeignKey(WarehouseInventory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    
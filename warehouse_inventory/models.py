from __future__ import unicode_literals

from django.db import models

# Create your models here.
class WarehouseInventory(models.Model):
    item_number = models.IntegerField(unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    quantity = models.IntegerField()
    description = models.CharField(max_length=250)
    
    

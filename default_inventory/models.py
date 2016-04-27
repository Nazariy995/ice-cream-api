from __future__ import unicode_literals

from django.db import models

# Create your models here.

class DefaultInventory(models.Model):
    item_number = models.IntegerField(unique=True)
    quantity = models.IntegerField()

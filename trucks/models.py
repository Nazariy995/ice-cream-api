
from django.db import models

# Create your models here.

class Truck(models.Model):
    truck_number = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add= True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)
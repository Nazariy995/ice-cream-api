
from django.db import models

# Create your models here.

class Truck(models.Model):
    truck_number = models.IntegerField(max_length = 4)
    available = models.NullBooleanField
    model = models.CharField(max_length = 50)
    year = models.IntegerField(max_length = 4)
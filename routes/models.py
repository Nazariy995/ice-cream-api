
from django.db import models
from django.utils import timezone

# Create your models here.

class Route(models.Model):
    route_number = models.IntegerField(max_length = 4)
    city_list = models.CharField(max_length = 30)
    trucks = models.IntegerField(max_length = 4)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)

from django.db import models
from django.utils import timezone

# Create your models here.

class Route(models.Model):
    route_number = models.IntegerField(unique=True)
    date_added = models.DateTimeField(auto_now_add= True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)

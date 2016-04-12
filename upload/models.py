from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Upload(models.Model):
    sequence_number = models.IntegerField()
    type_of_file = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add= True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Upload(models.Model):
    sequence_number = models.IntegerField()
    file_type = models.CharField(max_length=100)
    date_added = models.DateField(null=False)

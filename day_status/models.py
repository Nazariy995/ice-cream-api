from django.db import models

# Create your models here.

class DayStatus(models.Model):
    login_date = models.DateField(null=False, auto_now_add=True)


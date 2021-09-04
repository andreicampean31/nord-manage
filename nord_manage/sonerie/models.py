from django.db import models


class Sonerii(models.Model):
    denumire = models.CharField(max_length=200)
    pin = models.CharField(max_length=200)
    versiune = models.CharField(max_length=200)
    ore = models.CharField(max_length=200)
    status = models.BooleanField()
# Create your models here.

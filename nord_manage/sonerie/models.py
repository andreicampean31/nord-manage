from django.db import models


class Info_Sonerii(models.Model):
    denumire = models.CharField(max_length=200)
    pin = models.CharField(max_length=200)
    versiune = models.CharField(max_length=200)
    status = models.BooleanField()
    
class Ore_Sonerii(models.Model):
    soneria = models.ForeignKey(Info_Sonerii, on_delete=models.CASCADE)
    ora = models.TimeField()
    status = models.BooleanField()
# Create your models here.

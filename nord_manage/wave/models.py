from django.db import models
from django.utils import timezone

# Create your models here.

class Date_Placi(models.Model):
    cod_placa = models.CharField(max_length=200)
    min_placa = models.FloatField()
    multiplication_factor = models.IntegerField(default=1)
    def __str__(self):
        return self.cod_placa

class Productie(models.Model):
    cod_placa = models.ForeignKey(Date_Placi, on_delete=models.CASCADE)
    linie_productie = models.CharField(max_length=2)
    data = models.DateTimeField()
    multi_factor = models.IntegerField(default=1)

    def multiply(self, count):
        return count*self.multi_factor
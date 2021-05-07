from django.db import models
from django.utils import timezone

# Create your models here.

class Date_Placi(models.Model):
    cod_placa = models.CharField(max_length=200)
    min_placa = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.cod_placa

class Productie(models.Model):
    cod_placa = models.ForeignKey(Date_Placi, on_delete=models.CASCADE)
    linie_productie = models.CharField(max_length=2)
    data = models.DateTimeField()
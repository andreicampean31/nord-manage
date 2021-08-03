from django.db import models

class Date_Placi(models.Model):
    cod_placa = models.CharField(max_length=200)

class Defecte(models.Model):
    data = models.DateField()
    cod_placa = models.ForeignKey(Date_Placi, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=200)
    step_fail = models.CharField(max_length=200)
    defect = models.CharField(max_length=1000)
    problem = models.CharField(max_length=1000)
    component_phase_reference = models.CharField(max_length=200)
    action_performed = models.CharField(max_length=200)
    functional_test = models.BooleanField()
    security_test = models.BooleanField()
    tip_componenta = models.CharField(max_length=200)
    familia = models.CharField(max_length=200)
    commessa = models.CharField(max_length=200)
    produs_in = models.CharField(max_length=200)
    #anno
    #week
    #voci generiche
    #w.Filltro

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
    comp_ph_ref = models.CharField(max_length=200)
    act_perf = models.CharField(max_length=200)
    func_test = models.BooleanField()
    sec_test = models.BooleanField()
    tip_comp = models.CharField(max_length=200)
    familia = models.CharField(max_length=200)
    commessa = models.CharField(max_length=200)
    produs_in = models.CharField(max_length=200)
    voci = models.CharField(max_length=200)


class Temporary(models.Model):
    my_id = models.CharField(max_length=5)
    data = models.DateField()
    cod_placa = models.ForeignKey(Date_Placi, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=200)
    step_fail = models.CharField(max_length=200)
    defect = models.CharField(max_length=1000)
    problem = models.CharField(max_length=1000)
    comp_ph_ref = models.CharField(max_length=200)
    act_perf = models.CharField(max_length=200)
    func_test = models.BooleanField()
    sec_test = models.BooleanField()
    tip_comp = models.CharField(max_length=200)
    familia = models.CharField(max_length=200)
    commessa = models.CharField(max_length=200)
    produs_in = models.CharField(max_length=200)
    voci = models.CharField(max_length=200)

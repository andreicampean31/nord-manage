from django.shortcuts import render
from .models import Productie, Date_Placi
from django.db import connection


def home(request):
    cursor = connection.cursor()
    cursor.execute('''select cod_placa, count(*) as nr_buc
        from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.line_productie
      from wave_productie
               inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
      where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
        and wave_productie.line_productie = 1) as wpwdp
        group by cod_placa;''')
    results = cursor.fetchall()
    return render(request, 'wave/home.html', {'data': results})

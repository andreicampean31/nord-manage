from django.shortcuts import render
from .models import Productie, Date_Placi
from django.db import connection


def home(request):
    linia1 = connection.cursor()
    linia1.execute('''select cod_placa, count(*) as nr_buc
        from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.line_productie
      from wave_productie
               inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
      where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
        and wave_productie.line_productie = 1) as wpwdp
        group by cod_placa;''')
    results_linia1 = linia1.fetchall()

    linia2 = connection.cursor()
    linia2.execute('''select cod_placa, count(*) as nr_buc
        from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.line_productie
      from wave_productie
               inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
      where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
        and wave_productie.line_productie = 2) as wpwdp
        group by cod_placa;''')
    results_linia2 = linia2.fetchall()

    linia3 = connection.cursor()
    linia3.execute('''select cod_placa, count(*) as nr_buc
        from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.line_productie
      from wave_productie
               inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
      where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
        and wave_productie.line_productie = 3) as wpwdp
        group by cod_placa;''')
    results_linia3 = linia3.fetchall()

    context = {
      'linia1': results_linia1,
      'linia2': results_linia2,
      'linia3': results_linia3,
    }
    return render(request, 'wave/home.html', context)
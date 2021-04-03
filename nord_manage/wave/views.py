from django.shortcuts import render
from .models import Productie, Date_Placi
from django.db import connection
from django.http import JsonResponse

      
def home(request):
      #LINIA 1 
      #linia 1 rezultate pentru tabel
      linia1_tabel = connection.cursor()
      linia1_tabel.execute('''select cod_placa, count(*) as nr_buc
          from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.line_productie
        from wave_productie
                  inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
        where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
          and wave_productie.line_productie = 1) as wpwdp
          group by cod_placa;''')
      results_linia1_tabel = linia1_tabel.fetchall()

      #linia 1 rezultate pentru chart
      linia1_chart = connection.cursor()
      linia1_chart.execute('''select cod_placa, min_placa, count(*) as nr_buc
          from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.line_productie
        from wave_productie
                  inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
        where EXTRACT(HOUR FROM wave_productie.data) = EXTRACT(HOUR from now())
          and wave_productie.line_productie = 1) as wpwdp
          group by cod_placa;''')
      results_linia1_chart = linia1_chart.fetchall()

      min_lucrate_linia1 = 0
      for i in results_linia1_chart:
            min_lucrate_linia1 += i[1]*i[2]

      print(min_lucrate_linia1)

      #LINIA 2 
      #linia 2 rezultate pentru tabel
      linia2_tabel = connection.cursor()
      linia2_tabel.execute('''select cod_placa, count(*) as nr_buc
          from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.line_productie
        from wave_productie
                  inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
        where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
          and wave_productie.line_productie = 2) as wpwdp
          group by cod_placa;''')
      results_linia2_tabel = linia2_tabel.fetchall()

      #linia 2 rezultate pentru chart
      linia2_chart = connection.cursor()
      linia2_chart.execute('''select cod_placa, min_placa, extract(hour from data) as ora, extract(minute from data) as minute, count(*) as nr_buc
          from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.line_productie
        from wave_productie
                  inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
        where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
          and wave_productie.line_productie = 2) as wpwdp
          group by  EXTRACT(HOUR from data), cod_placa ;''')
      results_linia2_chart = linia2_chart.fetchall()

      j=0 #counter schimbare ora
      k=0 #counter schimbare jumatate de ora
      intrari_linia2 = [0]
      min_lucrate_linia2 = 0
      for i in results_linia2_chart:
        if (k==0 and i[4]>30) or (k==1 and i[4]<30):
          intrari_linia2.append(min_lucrate_linia2)
        if i[4]<=30:
              min_lucrate_linia2 += i[1]*i[4]
              print(min_lucrate_linia2)
              k=0
        else:
              min_lucrate_linia2 += i[1]*i[4]
              print(min_lucrate_linia2)
              k=1
      print(intrari_linia2) 
                        

      #print(min_lucrate_linia2)

      #LINIA 3 
      #linia 3 rezultate pentru tabel
      linia3_tabel = connection.cursor()
      linia3_tabel.execute('''select cod_placa, count(*) as nr_buc
          from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.line_productie
        from wave_productie
                  inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
        where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
          and wave_productie.line_productie = 3) as wpwdp
          group by cod_placa;''')
      results_linia3_tabel = linia3_tabel.fetchall()

      #linia 3 rezultate pentru chart
      linia3_chart = connection.cursor()
      linia3_chart.execute('''select cod_placa, min_placa, count(*) as nr_buc
          from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.line_productie
        from wave_productie
                  inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
        where EXTRACT(HOUR FROM wave_productie.data) = EXTRACT(HOUR from now())
          and wave_productie.line_productie = 3) as wpwdp
          group by cod_placa;''')
      results_linia3_chart = linia3_chart.fetchall()

      min_lucrate_linia3 = 0
      for i in results_linia3_chart:
            min_lucrate_linia3 += i[1]*i[2]

      print(min_lucrate_linia3)


      context = {
        'linia1_tabel': results_linia1_tabel,
        'linia1_chart': results_linia1_chart,

        'linia2_tabel': results_linia2_tabel,
        'linia2_chart': results_linia2_chart,

        'linia3_tabel': results_linia3_tabel,
        'linia3_chart': results_linia3_chart,
      }
      return render(request, 'wave/home.html', context)

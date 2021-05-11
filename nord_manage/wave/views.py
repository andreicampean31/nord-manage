from django.shortcuts import render
from .models import Productie, Date_Placi
from django.db import connection
from django.http import JsonResponse
from nord_manage.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.http import HttpResponse
from django.utils import timezone
import datetime
def home(request):

      

      #LINIA 1 
      #linia 1 rezultate pentru tabel
      linia1_tabel = connection.cursor()
      linia1_tabel.execute('''SELECT cod_placa, COUNT(*) as nr_buc, FLOOR(60/min_placa) as target
          FROM (SELECT wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.linie_productie
        FROM wave_productie
                  INNER JOIN wave_date_placi ON wave_productie.cod_placa_id = wave_date_placi.id
        WHERE CAST(wave_productie.data AS Date) = CAST(NOW() as Date)
          AND wave_productie.linie_productie = 1) AS productie_actuala
          GROUP BY cod_placa;''')
      results_linia1_tabel = linia1_tabel.fetchall()

      #LINIA 2 
      #linia 2 rezultate pentru tabel
      linia2_tabel = connection.cursor()
      linia2_tabel.execute('''SELECT cod_placa, COUNT(*) as nr_buc, FLOOR(60/min_placa) as target
          FROM (SELECT wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.linie_productie
        FROM wave_productie
                  INNER JOIN wave_date_placi ON wave_productie.cod_placa_id = wave_date_placi.id
        WHERE CAST(wave_productie.data AS Date) = CAST(NOW() as Date)
          AND wave_productie.linie_productie = 2) AS productie_actuala
          GROUP BY cod_placa;''')
      results_linia2_tabel = linia2_tabel.fetchall()             

      #LINIA 3
      #linia 3 rezultate pentru tabel
      linia3_tabel = connection.cursor()
      linia3_tabel.execute('''SELECT cod_placa, COUNT(*) as nr_buc, FLOOR(60/min_placa) as target
          FROM (SELECT wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.linie_productie
        FROM wave_productie
                  INNER JOIN wave_date_placi ON wave_productie.cod_placa_id = wave_date_placi.id
        WHERE CAST(wave_productie.data AS Date) = CAST(NOW() as Date)
          AND wave_productie.linie_productie = 3) AS productie_actuala
          GROUP BY cod_placa;''')
      results_linia3_tabel = linia3_tabel.fetchall()

      context = {
        'linia1': results_linia1_tabel,
        'linia2': results_linia2_tabel,
        'linia3': results_linia3_tabel,
      }
      return render(request, 'wave/home.html', context)


def efficency_chart(request):
  labels={
    'linia1': [],
    'linia2': [],
    'linia3': [],
  }
  data={
    'linia1': [0],
    'linia2': [0],
    'linia3': [0],
  }

  linia1 = connection.cursor()
  linia1.execute('''SELECT CONCAT(DATE_FORMAT(data, '%H:'), IF('30' > MINUTE(data), '00', '30')) AS 'Hour Interval',
       SUM(min_placa) AS 'Minutes Worked'
      FROM (select min_placa,data
          from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.linie_productie
             from wave_productie
                inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
            where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
                and wave_productie.linie_productie = 1) as wpwdp) as asd
              GROUP BY CONCAT(DATE_FORMAT(data, '%H:'), IF('30' > MINUTE(data), '00', '30'));''')
  results_linia1 = linia1.fetchall()

  for i in results_linia1:
    labels["linia1"].append(i[0])
    eficienta = i[1]*100/30
    data["linia1"].append(eficienta)

  linia2 = connection.cursor()
  linia2.execute('''SELECT CONCAT(DATE_FORMAT(data, '%H:'), IF('30' > MINUTE(data), '00', '30')) AS 'Hour Interval',
       SUM(min_placa) AS 'Minutes Worked'
      FROM (select min_placa,data
          from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.linie_productie
             from wave_productie
                inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
            where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
                and wave_productie.linie_productie = 2) as wpwdp) as asd
              GROUP BY CONCAT(DATE_FORMAT(data, '%H:'), IF('30' > MINUTE(data), '00', '30'));''')
  results_linia2 = linia2.fetchall()

  for i in results_linia2:
    labels["linia2"].append(i[0])
    eficienta = i[1]*100/30
    data["linia2"].append(eficienta)

  linia3 = connection.cursor()
  linia3.execute('''SELECT CONCAT(DATE_FORMAT(data, '%H:'), IF('30' > MINUTE(data), '00', '30')) AS 'Hour Interval',
       SUM(min_placa) AS 'Minutes Worked'
      FROM (select min_placa,data
          from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.linie_productie
             from wave_productie
                inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
            where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
                and wave_productie.linie_productie = 3) as wpwdp) as asd
              GROUP BY CONCAT(DATE_FORMAT(data, '%H:'), IF('30' > MINUTE(data), '00', '30'));''')
  results_linia3 = linia3.fetchall()

  for i in results_linia3:
    labels["linia3"].append(i[0])
    eficienta = i[1]*100/30
    data["linia3"].append(eficienta)

  return JsonResponse(data={
    'labels': labels,
    'data': data,
  })

def report_data(request):
  #LINIA 1 
  #linia 1 rezultate pentru tabel
  linia1_tabel = connection.cursor()
  linia1_tabel.execute('''SELECT cod_placa, COUNT(*) as nr_buc, FLOOR(60/min_placa) as target
      FROM (SELECT wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.linie_productie
    FROM wave_productie
              INNER JOIN wave_date_placi ON wave_productie.cod_placa_id = wave_date_placi.id
    WHERE CAST(wave_productie.data AS Date) = CAST(NOW() as Date)
      AND wave_productie.linie_productie = 1) AS productie_actuala
      GROUP BY cod_placa;''')
  results_linia1_tabel = linia1_tabel.fetchall()

  #LINIA 2 
  #linia 2 rezultate pentru tabel
  linia2_tabel = connection.cursor()
  linia2_tabel.execute('''SELECT cod_placa, COUNT(*) as nr_buc, FLOOR(60/min_placa) as target
      FROM (SELECT wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.linie_productie
    FROM wave_productie
              INNER JOIN wave_date_placi ON wave_productie.cod_placa_id = wave_date_placi.id
    WHERE CAST(wave_productie.data AS Date) = CAST(NOW() as Date)
      AND wave_productie.linie_productie = 2) AS productie_actuala
      GROUP BY cod_placa;''')
  results_linia2_tabel = linia2_tabel.fetchall()             

  #LINIA 3
  #linia 3 rezultate pentru tabel
  linia3_tabel = connection.cursor()
  linia3_tabel.execute('''SELECT cod_placa, COUNT(*) as nr_buc, FLOOR(60/min_placa) as target
      FROM (SELECT wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.linie_productie
    FROM wave_productie
              INNER JOIN wave_date_placi ON wave_productie.cod_placa_id = wave_date_placi.id
    WHERE CAST(wave_productie.data AS Date) = CAST(NOW() as Date)
      AND wave_productie.linie_productie = 3) AS productie_actuala
      GROUP BY cod_placa;''')
  results_linia3_tabel = linia3_tabel.fetchall()

  now = datetime.datetime.now()
  context = {
    'linia1': results_linia1_tabel,
    'linia2': results_linia2_tabel,
    'linia3': results_linia3_tabel,
    'ora': now.hour
  }

  subject = 'Raport orar Wave'
  from_email = EMAIL_HOST_USER
  to = 'omegagroup96@gmail.com'

  text_content = 'Raport orar Wave'
  mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
  html_template = get_template("wave/report_email.html").render(context)

  mail.attach_alternative(html_template, "text/html")
  mail.send()
  
  return HttpResponse(status = 201)

def insert_data(request, linie, cod_placa):
  now = timezone.now()
  print(now)
  
  cod_placa_id = Date_Placi.objects.get(cod_placa = cod_placa)
  print(cod_placa_id)
  insert_data = Productie(cod_placa_id = cod_placa_id.id, linie_productie = linie, data = now)
  insert_data.save()
  print(linie)

  return HttpResponse(status = 201)
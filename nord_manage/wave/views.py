from typing import DefaultDict
from django.shortcuts import render
from .models import Productie, Date_Placi
from django.db.models import Count, F
from django.db import connection
from django.http import JsonResponse
from nord_manage.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
import datetime
from .forms import DatePlaciForm
from math import floor

def day_total(numar_linii_productie):
  numar_linii_productie = 3
  context = {
    'linia1': None,
    'linia2': None,
    'linia3': None,
  }
  for linia in range(0, numar_linii_productie):
    today = datetime.date.today()

    today_entries = Productie.objects.filter(data__date=today, linie_productie=linia+1).values('cod_placa__cod_placa', 'multi_factor').annotate(count=Count('cod_placa'), total=Count('cod_placa')*F('multi_factor')).order_by('cod_placa_id')

    coduri_placi=[None] * len(today_entries)
    total_count=[0] * len(today_entries)

    for i in today_entries:
      cod_placa = i['cod_placa__cod_placa']
      total = i['total']

      for j in range(0, len(today_entries)):
        if coduri_placi[j] == cod_placa:
          total_count[j] += total
          break
        else:
          if coduri_placi[j] == None :
            coduri_placi[j] = cod_placa
            total_count[j] += total
            break

    coduri_placi_cleaned = list(filter(None, coduri_placi))
    total_count_cleaned = list(filter(None, total_count))
    
    final_array = [None] * len(coduri_placi_cleaned)
    
    for i in range(0, len(final_array)):
      
      target = Date_Placi.objects.filter(cod_placa = coduri_placi_cleaned[i]).values('min_placa')

      final_array[i] = {
        'cod_placa': coduri_placi_cleaned[i],
        'total': total_count_cleaned[i],
        'target': floor(60/target[0]['min_placa'])
        }

    context['linia' + str(linia+1)] = final_array
  return context

def home(request):
  return render(request, 'wave/home.html', context=day_total(3))

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
  numar_linii_productie = 3
  now = datetime.datetime.now()

  context_total = day_total(numar_linii_productie)

  context_last_hour = {
    'linia1': None,
    'linia2': None,
    'linia3': None,
    'ora_actuala': now.strftime('%H:%M'),
    'interval': str(now.hour-1) + ':00' + ' - ' + now.strftime('%H:' + '00'),
  }

  for linia in range(0, numar_linii_productie):

    today_entries = Productie.objects.filter(data__hour=now.hour-1, linie_productie=linia+1).values('cod_placa__cod_placa', 'multi_factor').annotate(count=Count('cod_placa'), total=Count('cod_placa')*F('multi_factor')).order_by('cod_placa_id')

    coduri_placi=[None] * len(today_entries)
    total_count=[0] * len(today_entries)

    for i in today_entries:
      cod_placa = i['cod_placa__cod_placa']
      total = i['total']

      for j in range(0, len(today_entries)):
        if coduri_placi[j] == cod_placa:
          total_count[j] += total
          break
        else:
          if coduri_placi[j] == None :
            coduri_placi[j] = cod_placa
            total_count[j] += total
            break

    coduri_placi_cleaned = list(filter(None, coduri_placi))
    total_count_cleaned = list(filter(None, total_count))
    
    final_array = [None] * len(coduri_placi_cleaned)
    
    for i in range(0, len(final_array)):
      
      target = Date_Placi.objects.filter(cod_placa = coduri_placi_cleaned[i]).values('min_placa')

      final_array[i] = {
        'cod_placa': coduri_placi_cleaned[i],
        'total': total_count_cleaned[i],
        'target': floor(60/target[0]['min_placa'])
        }

    context_last_hour['linia' + str(linia+1)] = final_array

  subject = 'Raport Wave ' + now.strftime('%H:%M')
  from_email = EMAIL_HOST_USER
  to = 'andreicampean@gmail.com'

  text_content = 'Raport orar Wave'
  mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
  html_template = get_template("wave/report_email.html").render({'total':context_total, 'last_hour': context_last_hour})

  mail.attach_alternative(html_template, "text/html")
  mail.send()
  
  return HttpResponse(status = 201)
  #return render(request, 'wave/report_email.html', context= {'total':context_total, 'last_hour': context_last_hour})

def insert_data(request, linie, cod_placa):
  now = timezone.now()
  
  placa_info = Date_Placi.objects.get(cod_placa = cod_placa)

  insert_data = Productie(cod_placa_id = placa_info.id, linie_productie = linie, data = now, multi_factor = placa_info.multiplication_factor)
  insert_data.save()

  return HttpResponse(status = 201)

def settings(request):
  lista_placi = Date_Placi.objects.order_by('cod_placa')
  context = {
    'lista': lista_placi
  }
  return render(request, 'wave/settings.html', context)

def date_placi_update(request):
  if request.method == 'POST':
    form = DatePlaciForm(request.POST)
    
    if form.is_valid():
      cod_placa = form.cleaned_data.get('cod_placa')
      min_placa = form.cleaned_data.get('min_placa')
      factor = form.cleaned_data.get('multiplication_factor')

      Date_Placi.objects.filter(cod_placa = cod_placa).update(min_placa = min_placa, multiplication_factor = factor)
      
      return HttpResponseRedirect('/wave/settings')
  else:
    form = DatePlaciForm()
  
  return HttpResponse(status=404)

def date_placi_delete(request, cod_placa):
  Date_Placi.objects.filter(cod_placa = cod_placa).delete()
  
  return HttpResponseRedirect('/wave/settings')

def date_placi_add(request):
  if request.method == 'POST':
    form = DatePlaciForm(request.POST)

    if form.is_valid():
      cod_placa = form.cleaned_data.get('cod_placa')
      min_placa = form.cleaned_data.get('min_placa')
      factor = form.cleaned_data.get('multiplication_factor')

      insert_code = Date_Placi(cod_placa = cod_placa, min_placa = min_placa, multiplication_factor = factor)
      insert_code.save()
      
      return HttpResponseRedirect('/wave/settings')
  else:
    form = DatePlaciForm()
  
  return HttpResponse(status = 404)

def custom_reports(request):
  lista_placi = Date_Placi.objects.order_by('cod_placa').values('cod_placa')
  context = {
    'lista': lista_placi
  }
  print(context)
  return render(request, 'wave/reports.html', context)
  
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
from .forms import DatePlaciForm, CustomReportForm
from math import floor


def count_total_productie(entries):
    coduri_placi = [None] * len(entries)
    total_count = [0] * len(entries)
    # print(entries)
    final_array = [None]
    for i in entries:
        cod_placa = i['cod_placa__cod_placa']
        total = i['total']

        for j in range(0, len(entries)):
            if coduri_placi[j] == cod_placa:
                total_count[j] += total
                break
            else:
                if coduri_placi[j] == None:
                    coduri_placi[j] = cod_placa
                    total_count[j] += total
                    break

        coduri_placi_cleaned = list(filter(None, coduri_placi))
        total_count_cleaned = list(filter(None, total_count))

        final_array = [None] * len(coduri_placi_cleaned)

        for i in range(0, len(final_array)):

            target = Date_Placi.objects.filter(
                cod_placa=coduri_placi_cleaned[i]).values('min_placa')

            final_array[i] = {
                'cod_placa': coduri_placi_cleaned[i],
                'total': total_count_cleaned[i],
                'target': floor(60/target[0]['min_placa'])
            }
    print(final_array)
    return final_array


def today_total(numar_linii_productie):
    numar_linii_productie = 3
    context = {
        'linia1': None,
        'linia2': None,
        'linia3': None
    }
    for linia in range(0, numar_linii_productie):
        today = datetime.date.today()

        today_entries = Productie.objects.filter(data__date=today, linie_productie=linia+1).values('cod_placa__cod_placa', 'multi_factor').annotate(
            count=Count('cod_placa'), total=Count('cod_placa')*F('multi_factor')).order_by('cod_placa_id')

        context['linia' + str(linia+1)] = count_total_productie(today_entries)

    return context


def home(request):
    return render(request, 'wave/home.html', context=today_total(3))


def realtimeview(request):
    return render(request, 'wave/realtime.html', context=today_total(3))


def efficency_chart(request):
    labels = {
        'linia1': [],
        'linia2': [],
        'linia3': [],
    }
    data = {
        'linia1': [0],
        'linia2': [0],
        'linia3': [0],
    }

    linia1 = connection.cursor()
    linia1.execute('''SELECT CONCAT(DATE_FORMAT(data, '%H:'), IF('30' > MINUTE(data), '00', '30')) AS 'Hour Interval',
       SUM(min_placa*multiplication_factor) AS 'Minutes Worked'
      FROM (select min_placa,data, multiplication_factor
          from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.linie_productie, wave_date_placi.multiplication_factor
             from wave_productie
                inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
            where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
                and wave_productie.linie_productie = 1) as wpwdp) as asd
              GROUP BY CONCAT(DATE_FORMAT(data, '%H:'), IF('30' > MINUTE(data), '00', '30'));''')
    results_linia1 = sorted(linia1.fetchall())


    for i in results_linia1:
        labels["linia1"].append(i[0])
        eficienta = i[1]*100/30
        data["linia1"].append(eficienta)

    linia2 = connection.cursor()
    linia2.execute('''SELECT CONCAT(DATE_FORMAT(data, '%H:'), IF('30' > MINUTE(data), '00', '30')) AS 'Hour Interval',
       SUM(min_placa*multiplication_factor) AS 'Minutes Worked'
      FROM (select min_placa,data, multiplication_factor
          from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.linie_productie, wave_date_placi.multiplication_factor
             from wave_productie
                inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
            where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
                and wave_productie.linie_productie = 2) as wpwdp) as asd
              GROUP BY CONCAT(DATE_FORMAT(data, '%H:'), IF('30' > MINUTE(data), '00', '30'));''')
    results_linia2 = sorted(linia2.fetchall())

    for i in results_linia2:
        labels["linia2"].append(i[0])
        eficienta = i[1]*100/30
        data["linia2"].append(eficienta)

    linia3 = connection.cursor()
    linia3.execute('''SELECT CONCAT(DATE_FORMAT(data, '%H:'), IF('30' > MINUTE(data), '00', '30')) AS 'Hour Interval',
       SUM(min_placa*multiplication_factor) AS 'Minutes Worked'
      FROM (select min_placa,data, multiplication_factor
          from (select wave_date_placi.cod_placa, wave_date_placi.min_placa, wave_productie.data, wave_productie.linie_productie, wave_date_placi.multiplication_factor
             from wave_productie
                inner join wave_date_placi on wave_productie.cod_placa_id = wave_date_placi.id
            where CAST(wave_productie.data as Date) = CAST(NOW() as Date)
                and wave_productie.linie_productie = 3) as wpwdp) as asd
              GROUP BY CONCAT(DATE_FORMAT(data, '%H:'), IF('30' > MINUTE(data), '00', '30'));''')
    results_linia3 = sorted(linia3.fetchall())

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

    context_total = today_total(numar_linii_productie)

    context_last_hour = {
        'linia1': None,
        'linia2': None,
        'linia3': None,
        'ora_actuala': now.strftime('%H:%M'),
        'interval': str(now.hour-1) + ':00' + ' - ' + now.strftime('%H:' + '00'),
    }

    for linia in range(0, numar_linii_productie):

        today_entries = Productie.objects.filter(data__hour=now.hour-1, linie_productie=linia+1).values(
            'cod_placa__cod_placa', 'multi_factor').annotate(count=Count('cod_placa'), total=Count('cod_placa')*F('multi_factor')).order_by('cod_placa_id')

        coduri_placi = [None] * len(today_entries)
        total_count = [0] * len(today_entries)

        for i in today_entries:
            cod_placa = i['cod_placa__cod_placa']
            total = i['total']

            for j in range(0, len(today_entries)):
                if coduri_placi[j] == cod_placa:
                    total_count[j] += total
                    break
                else:
                    if coduri_placi[j] == None:
                        coduri_placi[j] = cod_placa
                        total_count[j] += total
                        break

        coduri_placi_cleaned = list(filter(None, coduri_placi))
        total_count_cleaned = list(filter(None, total_count))

        final_array = [None] * len(coduri_placi_cleaned)

        for i in range(0, len(final_array)):

            target = Date_Placi.objects.filter(
                cod_placa=coduri_placi_cleaned[i]).values('min_placa')

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
    html_template = get_template("wave/report_email.html").render(
        {'total': context_total, 'last_hour': context_last_hour})

    mail.attach_alternative(html_template, "text/html")
    mail.send()

    return HttpResponseRedirect('/wave')


def insert_data(request, linie, cod_placa):
    now = timezone.now()

    placa_info = Date_Placi.objects.get(cod_placa=cod_placa)

    insert_data = Productie(cod_placa_id=placa_info.id, linie_productie=linie,
                            data=now, multi_factor=placa_info.multiplication_factor)
    insert_data.save()

    return HttpResponse(status=201)


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

            Date_Placi.objects.filter(cod_placa=cod_placa).update(
                min_placa=min_placa, multiplication_factor=factor)

            return HttpResponseRedirect('/wave/settings')
    else:
        form = DatePlaciForm()

    return HttpResponse(status=404)


def date_placi_delete(request, cod_placa):
    
    if Productie.objects.filter(cod_placa_id__cod_placa = cod_placa).exists():
        return HttpResponseRedirect('/wave/settings/#errorDelete')
    else:
        Date_Placi.objects.filter(cod_placa=cod_placa).delete()

    return HttpResponseRedirect('/wave/settings')


def date_placi_add(request):
    if request.method == 'POST':
        form = DatePlaciForm(request.POST)

        if form.is_valid():
            cod_placa = form.cleaned_data.get('cod_placa')
            min_placa = form.cleaned_data.get('min_placa')
            factor = form.cleaned_data.get('multiplication_factor')

            coduri_existente = Date_Placi.objects.all().values('cod_placa')

            for i in coduri_existente:
                if i['cod_placa'] == cod_placa:
                    return HttpResponseRedirect('/wave/settings/#errorAdd')

            insert_code = Date_Placi(
                cod_placa=cod_placa, min_placa=min_placa, multiplication_factor=factor)
            insert_code.save()

            return HttpResponseRedirect('/wave/settings')
    else:
        form = DatePlaciForm()

    return HttpResponse(status=404)


def custom_reports(request):
    lista_placi = Date_Placi.objects.order_by('cod_placa').values('cod_placa')
    context = {
        'lista': lista_placi
    }
    return render(request, 'wave/reports.html', context)


def custom_reports_result(request):
    if request.method == 'POST':
        form = CustomReportForm(request.POST)

        if form.is_valid():
            lista_coduri = request.POST.getlist('lista_coduri')
            date_range = form.cleaned_data.get('date_range')

            i = 0
            str_start_date = ''
            str_end_date = ''
            while i < 23:
                if(date_range[i] != ' ' or date_range[i] != '-'):
                    if i < 10:
                        str_start_date +=  date_range[i]
                    elif i >= 13:
                        str_end_date += date_range[i]
                i += 1

            str_start_date += ' 00:00:00'
            str_end_date += ' 23:59:59'

            start_date = datetime.datetime.strptime(
                str_start_date, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            end_date = datetime.datetime.strptime(
                str_end_date, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

            entries = Productie.objects.filter(cod_placa_id__cod_placa__in=lista_coduri, data__gte=start_date, data__lte=end_date).values(
                'cod_placa__cod_placa', 'multi_factor').annotate(count=Count('cod_placa'), total=Count('cod_placa')*F('multi_factor')).order_by('cod_placa_id')

            custom_report = count_total_productie(entries)
            lista_placi = Date_Placi.objects.order_by(
                'cod_placa').values('cod_placa')

            date_range = ''
            date_range += str_start_date[0:10]
            date_range += ' - '
            date_range += str_end_date[0:10]

            if str_start_date[0:10] == str_end_date[0:10]:
                date_range = str_start_date[0:10]

            print(date_range)
            now = datetime.datetime.now()
            print(now)
            if custom_report != [None]:
                context = {
                    'lista': lista_placi,
                    'result': custom_report,
                    'interval': date_range
                }
            else:
                context = {
                    'lista': lista_placi,
                    'interval': date_range
                }

            return render(request, 'wave/reports.html', context)

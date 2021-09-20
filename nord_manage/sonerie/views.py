from decimal import InvalidOperation
#from nord_manage import sonerie
from django.db import connections
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Info_Sonerii, Ore_Sonerii
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def home(request):
    lista_sonerii = Info_Sonerii.objects.values('id', 'denumire', 'status')

    
    sonerii = [None]*len(lista_sonerii)
    status = [None]*len(lista_sonerii)
    j=0
    for i in lista_sonerii:
        sonerii[j] = i['denumire']
        status[j] = i['status']
        j += 1
    
    context = {
        'zipped': zip(sonerii, status)
    }
    #print(context)
    return render(request, 'sonerie/home.html', context)
    #return JsonResponse({'status': 202})

def getAlarms(request):
    if request.method == 'GET':
        sonerii = Info_Sonerii.objects.values('denumire', 'status')
        
        denumiri = []
        status = []
        for i in sonerii:
            denumiri.append(i['denumire'])
            status.append(i['status'])
            
    return JsonResponse({
        'denumiri': denumiri,
        'status': status
    })
    
@csrf_exempt
def getSettings(request):
    if request.method == 'GET':
        denumire = request.GET.get('sonerie')
        
        setari = Info_Sonerii.objects.filter(denumire = denumire)
        ore = Ore_Sonerii.objects.filter(soneria_id__denumire = denumire)
        
        lista_ore = []
        status = []
        
        for i in ore:
            lista_ore.append(i.ora)
            status.append(i.status)
            
        #ore = setari[0].ore
    return JsonResponse({
        'id': setari[0].id,
        'denumire': setari[0].denumire,
        'pin': setari[0].pin,
        'versiune': setari[0].versiune,
        'ore': lista_ore,
        'status': status
        })

@csrf_exempt
def updateSettings(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        denumire = request.POST.get('denumire')
        pin = request.POST.get('pin')
        ore_active = request.POST.getlist('alarme_active[]')
        ore_inactive = request.POST.getlist('alarme_inactive[]')
        
        alarme_existente = Ore_Sonerii.objects.filter(soneria_id__denumire = denumire)
        print((len(ore_active)+len(ore_inactive)))
        print(len(alarme_existente))
        if (len(ore_active)+len(ore_inactive)) < len(alarme_existente):
            ore_total = ore_active + ore_inactive
            for i in alarme_existente:
                print(i.ora)
                k=0
                for j in ore_total:
                    print(j)
                    if i.ora == j:
                        k=1
                        break
                        
                if k == 0:
                    Ore_Sonerii.objects.filter(soneria_id__denumire = denumire, ora = i.ora).delete()
        
        #ore_noi = request.POST.getlist('alarme_noi[]')
        
        version = Info_Sonerii.objects.values('versiune')
        print(version[0]['versiune'])
        Info_Sonerii.objects.all().update(versiune = int(version[0]['versiune'])+1)
        
        Info_Sonerii.objects.filter(id = id).update(denumire = denumire, pin = pin)
        
        for i in ore_active:
            k=0
            for j in ore_active:
                if i==j:
                    k += 1
            for j in ore_inactive:
                if i==j:
                    k += 1
            if k > 1:
                return JsonResponse({'status': 404, 'desc': 'duplicate'})
            
        for i in ore_inactive:
            k=0
            for j in ore_active:
                if i==j:
                    k += 1
            for j in ore_inactive:
                if i==j:
                    k += 1
            if k > 1:
                return JsonResponse({'status': 404, 'desc': 'duplicate'})
        
        for i in ore_active:
            ora = Ore_Sonerii.objects.filter(soneria_id = id, ora = i)
            if ora:
                if ora[0].status == False:
                    Ore_Sonerii.objects.filter(soneria_id = id, ora = i).update(status = True)
                    
            else:
                alarma_noua = Ore_Sonerii(soneria_id = id, ora = i, status = True)
                alarma_noua.save()
            
        
        for i in ore_inactive:
            ora = Ore_Sonerii.objects.filter(soneria_id = id, ora = i)
            if ora:
                if ora[0].status == True:
                    Ore_Sonerii.objects.filter(soneria_id = id, ora = i).update(status = False)
            else:
                alarma_noua = Ore_Sonerii(soneria_id = id, ora = i, status = False)
                alarma_noua.save()
                
        if ore_active == []:
            Info_Sonerii.objects.filter(denumire = denumire).update(status = False)
            Ore_Sonerii.objects.filter(soneria_id = id).delete()
        else:
            Info_Sonerii.objects.filter(denumire = denumire).update(status = True)
            
        if ore_active != []:
            Info_Sonerii.objects.filter(denumire = denumire).update(status = True)
            

        
    return JsonResponse({'stauts': 202})
def ardu_get_settings(request):
    if request.method == 'GET':
        setari = Info_Sonerii.objects.all()
        #ore = Ore_Sonerii.objects.all()
            
        setari_json = {
            'status': 202,
            'names': [None]*len(setari),
            'pins': [None]*len(setari),
            'versiune': setari[0].versiune,
            'status': [None]*len(setari),
            'ore': [None]*len(setari)
        }
        
        for i in range(0, len(setari)):
            ore = Ore_Sonerii.objects.filter(soneria_id__denumire = setari[i].denumire, status = True)
        
            ore_list = [None] * len(ore)
            for j in range(0, len(ore)):
                time = str(ore[j].ora)
                ore_list[j] = (int(time[0:2]), int(time[3:5]), int(time[6:8]))
                
            #print(ore_str)
            #print(ore)
            setari_json['names'][i] = setari[i].denumire
            setari_json['pins'][i] = setari[i].pin
            setari_json['status'][i] = setari[i].status
            setari_json['ore'][i] = ore_list
        
    return JsonResponse(setari_json)
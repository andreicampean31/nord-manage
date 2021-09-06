
from django.db import connections
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Info_Sonerii, Ore_Sonerii
from django.views.decorators.csrf import csrf_exempt

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
        #ore_noi = request.POST.getlist('alarme_noi[]')
        
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
            

        
    return JsonResponse({'stauts': 202})
def ardu(request):
    #return HttpResponse(status = 202)
    
    return JsonResponse({'status': 202, 'version': 'v1.2'})
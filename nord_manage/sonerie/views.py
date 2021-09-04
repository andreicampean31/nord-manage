from django.db import connections
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Sonerii

def home(request):
    lista_sonerii = Sonerii.objects.values('denumire', 'status')

    
    sonerii = [None]*len(lista_sonerii)
    status = [None]*len(lista_sonerii)
    j=0
    for i in lista_sonerii:
        print(i['denumire'])
        sonerii[j] = i['denumire']
        status[j] = i['status']
        j += 1
    
    context = {
        'zipped': zip(sonerii, status)
    }
    #print(context)
    return render(request, 'sonerie/home.html', context)
    #return JsonResponse({'status': 202})

def getSettings(request):
    if request.method == 'GET':
        denumire = request.GET.get('sonerie')
        
        setari = Sonerii.objects.filter(denumire = denumire)
        print(setari[0].versiune)
        
        ore = setari[0].ore
    return JsonResponse({
        'status': 202,
        'denumire': setari[0].denumire,
        'pin': setari[0].pin,
        'versiune': setari[0].versiune,
        'ore': ore.split(","),
        'status': setari[0].status
        })
# Create your views here.

def ardu(request):
    #return HttpResponse(status = 202)
    
    return JsonResponse({'status': 202, 'version': 'v1.2'})
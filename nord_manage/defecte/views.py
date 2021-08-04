from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Defecte
import pandas 
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    return render(request, 'defecte/home.html')

def import_defecte(request):
    return render(request, 'defecte/import.html')

@csrf_exempt
def import_excel(request):
    if request.method == 'POST':
        fisier = request.FILES.get('file')

        excel_data = pandas.read_excel(fisier, parse_dates=['DATA'], sheet_name='Foglio1')
        json_str = excel_data.to_json(date_format='iso')    
        print(json_str)
    return JsonResponse(json_str, safe=False)
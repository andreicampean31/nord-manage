from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Defecte
# Create your views here.
def index(request):
    return render(request, 'defecte/home.html')

def import_defecte(request):
    return render(request, 'defecte/import.html')

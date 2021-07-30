from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request, 'defecte/home.html')

def import_defecte(request):
    return render(request, 'defecte/import.html')
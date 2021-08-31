from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse(status = 202)
# Create your views here.

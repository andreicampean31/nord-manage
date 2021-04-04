from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home, name='wave-home'),
    path('efficency-chart', views.efficency_chart, name='efficency-chart')
]
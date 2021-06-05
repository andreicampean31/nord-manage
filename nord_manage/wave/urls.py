from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home, name='wave-home'),
    path('efficency-chart/', views.efficency_chart, name='efficency-chart'),
    path('email_report/', views.report_data, name='wave-hour-report'),
    path('insert_data/<linie>&<cod_placa>/', views.insert_data, name='wave-insert-data'),
    path('settings/', views.settings, name = 'wave-settings'),
    path('settings/date-placi-update/', views.date_placi_update, name = 'date-placi-update'),
]
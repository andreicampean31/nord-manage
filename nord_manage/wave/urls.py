from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='wave-home'),
    path('efficency-chart', views.efficency_chart, name='efficency-chart'),
    path('insert_data/<linie>&<cod_placa>/',
         views.insert_data, name='wave-insert-data'),
    path('settings/', views.settings, name='wave-settings'),
    path('settings/date-placi-update/',
         views.date_placi_update, name='date-placi-update'),
    path('settings/date-placi-delete/<cod_placa>/',
         views.date_placi_delete, name='date-placi-delete'),
    path('settings/date-placi-add/', views.date_placi_add, name='date-placi-add'),
    path('reports/', views.custom_reports, name='wave-custom-reports'),
    path('reports/results', views.custom_reports_result,
         name='custom-reports-results'),
    path('realtimeview/', views.realtimeview, name='wave-realtimeview'),
    path('liveData/<linia>', views.liveData, name = 'wave-liveData')
]


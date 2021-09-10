from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='sonerie-home'),
    path('getAlarms', views.getAlarms, name='sonerie-getAlarms'),
    path('getSettings/', views.getSettings, name='sonerie-getsettings'),
    path('updateSettings/', views.updateSettings, name='sonerie-updateSettings'),
    path('arduGetSettings/', views.ardu_get_settings, name='sonerie-arduGetSettings')
    #path('import/update/', views.update, name='defecte-update')
]

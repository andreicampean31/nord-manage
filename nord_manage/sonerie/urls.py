from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='sonerie-home'),
    #path('import/update/', views.update, name='defecte-update')
]

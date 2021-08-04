from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='defecte-home'),
    path('import/', views.import_defecte, name='defecte-import' ),
    path('import/upload/', views.import_excel, name='defecte-upload' ),
    #path('import/update/', views.update, name='defecte-update')
]

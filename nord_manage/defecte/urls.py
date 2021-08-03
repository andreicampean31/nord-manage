from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='defecte-home'),
    path('import/', views.import_defecte, name='defecte-import' ),
    #path('import/upload/', views.upload_file, name='defecte-upload' ),
]

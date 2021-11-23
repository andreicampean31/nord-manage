from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='defecte-home'),
    path('update/', views.update, name='defecte-update'),
    path('addDefect/', views.addDefect, name='defecte-addDefect'),
    path('import/', views.import_defecte, name='defecte-import' ),
    path('import/upload/', views.import_excel, name='defecte-upload' ),
    path('import/clear/', views.clearDB, name='defecte-clearDB'),
    path('import/showTemp/', views.show_temp, name='defecte-showTemp'),
    path('import/updateTemp/', views.update_temp, name='defecte-updateTemp'),
    path('import/saveImport/', views.save_import, name='defecte-saveImport'),
    path('showHome/', views.show_home, name='defecte-showHome'),
    #path('import/update/', views.update, name='defecte-update')
]

from django.shortcuts import render
from .models import Productie

def home(request):
    test = '''
    SELECT * FROM wave_productie
    WHERE cod_placa_id=
                (SELECT id FROM wave_date_placi WHERE cod_placa='001.002')
        AND CAST(data as Date) = CAST(CURRENT_TIMESTAMP as Date )
    '''
    context = {    
        'date': Productie.objects.raw(test)
    }
    return render(request, 'wave/home.html', context)

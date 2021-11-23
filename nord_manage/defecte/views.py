from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from .models import Defecte, Date_Placi, Temporary
import pandas
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
    return render(request, 'defecte/home.html')


def import_defecte(request):
    return render(request, 'defecte/import.html')


@csrf_exempt
def import_excel(request):
    if request.method == 'POST':
        fisier = request.FILES.get('file')

        excel_data = pandas.read_excel(
            fisier, parse_dates=['DATA'], sheet_name='Foglio1')
        json_str = excel_data.to_json(date_format='iso')

        len = excel_data.shape[0]
        
        if Temporary.objects.all().exists():
            return JsonResponse({'status': 404})

        for i in range(0, len):
            try:
                id_placa = Date_Placi.objects.get(
                    cod_placa=excel_data['PRODUCT CODE'][i])
            except Date_Placi.DoesNotExist:
                id_placa = 0

            if id_placa == 0:
                cod_nou_insert = Date_Placi(
                    cod_placa=excel_data['PRODUCT CODE'][i])
                cod_nou_insert.save()
                id_placa = Date_Placi.objects.get(
                    cod_placa=excel_data['PRODUCT CODE'][i])
            print(id_placa.id)
            print(excel_data[' COMPONENT PHASE REFERENCE'][i])

            if excel_data['FUNCTIONAL TEST'][i] == 'PASS':
                functional_test = True
            else:
                functional_test = False

            if excel_data['SECURITY TEST'][i] == 'PASS':
                security_test = True
            else:
                security_test = False

            insert_temp = Temporary(my_id = i+1, data=excel_data['DATA'][i], cod_placa_id=id_placa.id, barcode=excel_data['BARCODE'][i], step_fail=excel_data['PHASE'][i], defect=excel_data['DEFECT'][i],
                                    problem=excel_data['PROBLEM'][i], comp_ph_ref=excel_data[' COMPONENT PHASE REFERENCE'][i], act_perf=excel_data['ACTION PERFORMED'][i], func_test=functional_test, sec_test=security_test)
            insert_temp.save()
            #print(excel_data['PRODUCT CODE'][i])

    return JsonResponse({'status': 202})

def show_temp(request):
    datas = Temporary.objects.values('my_id', 'data', 'barcode', 'step_fail', 'defect', 'problem', 'comp_ph_ref', 'act_perf', 'func_test', 'sec_test', 'tip_comp', 'familia', 'commessa', 'produs_in', 'voci', 'cod_placa__cod_placa')

    data = [dict() for number in range(len(datas))]

    for i in range(0, len(datas)):
        data[i]['id'] = datas[i]['my_id']
        data[i]['data'] = datas[i]['data']
        data[i]['barcode'] = datas[i]['barcode']
        data[i]['step_fail'] = datas[i]['step_fail']
        data[i]['defect'] = datas[i]['defect']
        data[i]['problem'] = datas[i]['problem']
        data[i]['comp_ph_ref'] = datas[i]['comp_ph_ref']
        data[i]['act_perf'] = datas[i]['act_perf']
        data[i]['func_test'] = datas[i]['func_test']
        data[i]['sec_test'] = datas[i]['sec_test']
        data[i]['tip_comp'] = datas[i]['tip_comp']
        data[i]['familia'] = datas[i]['familia']
        data[i]['commessa'] = datas[i]['commessa']
        data[i]['produs_in'] = datas[i]['produs_in']
        data[i]['voci'] = datas[i]['voci']
        data[i]['cod_placa'] = datas[i]['cod_placa__cod_placa']

    return JsonResponse({"data": data}, safe=False)


def clearDB(request):
    Temporary.objects.all().delete()
    if Temporary.objects.all().exists():
        return JsonResponse({'status': 404})
    return JsonResponse({'status': 202})

@csrf_exempt
def update_temp(request):
    if request.method == 'POST':
        edit_values = dict(request.POST.items())
        if edit_values['func_test'] == 'true':
            func_test = True
        else:
            func_test = False

        if edit_values['sec_test'] == 'true':
            sec_test = True
        else:
            sec_test = False
        Temporary.objects.filter(my_id = edit_values['id']).update(defect = edit_values['defect'], problem = edit_values['problem'], comp_ph_ref = edit_values['comp_ph_ref'], act_perf = edit_values['act_perf'], func_test = func_test, sec_test = sec_test, tip_comp = edit_values['tip_comp'], familia = edit_values['familia'], commessa = edit_values['commessa'], produs_in = edit_values['produs_in'], voci = edit_values['voci'])
        #print(edit_values['id'])
        
        
    return JsonResponse({"status": 202})

@csrf_exempt
def update(request):
    if request.method == 'POST':
        edit_values = dict(request.POST.items())
        if edit_values['func_test'] == 'true':
            func_test = True
        else:
            func_test = False

        if edit_values['sec_test'] == 'true':
            sec_test = True
        else:
            sec_test = False
        
        Defecte.objects.filter(id = edit_values['id']).update(defect = edit_values['defect'], problem = edit_values['problem'], comp_ph_ref = edit_values['comp_ph_ref'], act_perf = edit_values['act_perf'], func_test = func_test, sec_test = sec_test, tip_comp = edit_values['tip_comp'], familia = edit_values['familia'], commessa = edit_values['commessa'], produs_in = edit_values['produs_in'], voci = edit_values['voci'])
    #print(edit_values)
    
    return JsonResponse({"status": 202})

@csrf_exempt
def addDefect(request):
    if request.method == 'POST':
        add_values = dict(request.POST.items())
        print(add_values['code'])
        if add_values['func_test'] == 'PASS':
            functional_test = True
        else:
            functional_test = False

        if add_values['sec_test'] == 'PASS':
            security_test = True
        else:
            security_test = False
            
        cod_placa = Date_Placi.objects.get(cod_placa = add_values['code'])
        
        insert_value = Defecte(data=add_values['data'], cod_placa_id=cod_placa.id, barcode=add_values['barcode'], step_fail=add_values['step_fail'], defect=add_values['defect'],
                                    problem=add_values['problem'], comp_ph_ref=add_values['comp_ph_ref'], act_perf=add_values['act_perf'], func_test=functional_test, sec_test=security_test)
        insert_value.save()
        
    return JsonResponse({"status": 202})
        

def save_import(request):
    temp_data = Temporary.objects.all()
    #print(temp_data)
    if not temp_data:
        print(temp_data)
        return JsonResponse({"status": 404, "message": "Niciun fisier in memorie!"})

    
    for i in range(0, len(temp_data)):
        print(temp_data[i].data)
        new_data = Defecte(data = temp_data[i].data, cod_placa = temp_data[i].cod_placa, barcode = temp_data[i].barcode, step_fail = temp_data[i].step_fail, defect = temp_data[i].defect, problem = temp_data[i].problem, comp_ph_ref = temp_data[i].comp_ph_ref, act_perf = temp_data[i].act_perf, func_test = temp_data[i].func_test, sec_test = temp_data[i].sec_test, tip_comp = temp_data[i].tip_comp, familia = temp_data[i].familia, commessa = temp_data[i].commessa, produs_in = temp_data[i].produs_in, voci = temp_data[i].voci)
        new_data.save()
        Temporary.objects.all().delete()
    #new_data = Defecte()



    return JsonResponse({"status": 202, "message": "Import reusit!"})

def show_home(request):
    datas = Defecte.objects.values('id', 'data', 'barcode', 'step_fail', 'defect', 'problem', 'comp_ph_ref', 'act_perf', 'func_test', 'sec_test', 'tip_comp', 'familia', 'commessa', 'produs_in', 'voci', 'cod_placa__cod_placa')

    data = [dict() for number in range(len(datas))]

    for i in range(0, len(datas)):
        data[i]['id'] = datas[i]['id']
        data[i]['data'] = datas[i]['data']
        data[i]['barcode'] = datas[i]['barcode']
        data[i]['step_fail'] = datas[i]['step_fail']
        data[i]['defect'] = datas[i]['defect']
        data[i]['problem'] = datas[i]['problem']
        data[i]['comp_ph_ref'] = datas[i]['comp_ph_ref']
        data[i]['act_perf'] = datas[i]['act_perf']
        data[i]['func_test'] = datas[i]['func_test']
        data[i]['sec_test'] = datas[i]['sec_test']
        data[i]['tip_comp'] = datas[i]['tip_comp']
        data[i]['familia'] = datas[i]['familia']
        data[i]['commessa'] = datas[i]['commessa']
        data[i]['produs_in'] = datas[i]['produs_in']
        data[i]['voci'] = datas[i]['voci']
        data[i]['cod_placa'] = datas[i]['cod_placa__cod_placa']

    return JsonResponse({"data": data}, safe=False)